from typing import Annotated

from fastapi import Depends

from services.email_service.mailing import MailService
from services.email_service.connectors import AMQPMailConnector


async def get_amqp_mail_connector() -> AMQPMailConnector:
    return AMQPMailConnector()


async def get_mail_client_service(
    amqp_mail_connector: Annotated[AMQPMailConnector, Depends(get_amqp_mail_connector)]
) -> MailService:
    return MailService(amqp_mail_connector)
