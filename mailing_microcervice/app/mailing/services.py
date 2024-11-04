import aio_pika
import json
import uuid

from mailing.clients import MailClient
from mailing.connectors import AMQPMailConnector


class MailService:
    _EMAIL_CONSUME_ROUTING_KEY = "email_service_queue"
    _EMAIL_CALLBACK_ROUTING_KEY = "email_service_callback"
    _amqp_mail_connector = AMQPMailConnector
    _mail_client = MailClient()

    def send_email(self, subject: str, text: str, to: str) -> None:
        self._mail_client.send_email_message(subject, text, to)

    async def consume_mail_from_queue(self, message: aio_pika.IncomingMessage):
        corellation_id = message.correlation_id
        try:
            # SOME ...
            print(message)
            await message.ack()
            await self._make_amqp_message_callback(corellation_id)
        except Exception as e:
            await message.nack()
            await self._make_amqp_message_callback(corellation_id, False, str(e))
            raise

    async def _make_amqp_message_callback(
        self,
        corellation_id: str | None,
        succeeded: bool = True,
        err_message: str = "Successful!",
    ):
        message = await self._prepare_amqp_message_callback(corellation_id, succeeded, err_message)
        async with self._amqp_mail_connector() as connector:
            await connector.channel.declare_queue(
                name=self._EMAIL_CALLBACK_ROUTING_KEY,
                durable=True,
            )
            await connector.channel.default_exchange.publish(
                message=message,
                routing_key=self._EMAIL_CALLBACK_ROUTING_KEY,
            )

    async def _prepare_amqp_message_callback(
        self,
        corellation_id,
        succeeded,
        err_message,
    ) -> aio_pika.Message:
        email_body: dict = {
            "task": corellation_id,
            "status": succeeded,
            "message": err_message,
        }
        message = aio_pika.Message(
            body=json.dumps(email_body).encode(),
            correlation_id=str(uuid.uuid4()),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        return message
