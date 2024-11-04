import json
import uuid

import aio_pika

from services.email_service.schemas import MailCallbackHandlerSchema
from services.email_service.connectors import AMQPMailConnector


class MailService:
    EMAIL_ROUTING_KEY = "email_service_queue"

    def __init__(self, amqp_connector: AMQPMailConnector) -> None:
        self.amqp_connector = amqp_connector

    async def send_email(self, to: str, email_text: str, subject: str) -> None:
        message: aio_pika.Message = await self._prepare_message(to, email_text, subject)
        async with self.amqp_connector as connector:
            await connector.channel.declare_queue(
                name=self.EMAIL_ROUTING_KEY,
                durable=True,
            )
            await connector.channel.default_exchange.publish(
                message=message,
                routing_key=self.EMAIL_ROUTING_KEY,
            )

    async def _prepare_message(self, to: str, email_text: str, subject: str) -> aio_pika.Message:
        email_body: dict = {
            "message": email_text,
            "user_email": to,
            "subject": subject,
        }
        message = aio_pika.Message(
            body=json.dumps(email_body).encode(),
            correlation_id=str(uuid.uuid4()),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        return message

    @classmethod
    async def consume_mail_from_queue(cls, message: aio_pika.IncomingMessage):
        try:
            email_body = MailCallbackHandlerSchema(**json.loads(message.body.decode()))
            print(email_body.message)  # TODO do something
            if email_body.status is False:
                print(email_body.message)
                pass  # TODO do something
            await message.ack()
        except Exception:
            await message.reject(requeue=True)
            raise
