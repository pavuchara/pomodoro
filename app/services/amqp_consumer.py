import aio_pika

import settings
from services.email_service.mailing import MailService


CONSUME_QUEUE_MAPPER = {
    "email_service_callback": MailService.consume_mail_from_queue,
}


async def make_amqp_consumers():
    connection = await aio_pika.connect_robust(settings.AMQP_URL)
    channel = await connection.channel()
    for queue_name, callback_func in CONSUME_QUEUE_MAPPER.items():
        queue = await channel.declare_queue(
            name=queue_name,
            durable=True,
        )
        await queue.consume(callback_func, no_ack=False)
    return connection, channel
