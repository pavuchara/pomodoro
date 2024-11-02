import aio_pika

import settings


class AMQPMailConnector:

    def __init__(self, connection=None, channel=None) -> None:
        self.connection = connection
        self.channel = channel

    async def __aenter__(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(settings.AMQP_URL)
        if self.channel is None:
            self.channel = await self.connection.channel()
        return self

    async def __aexit__(self, ext_type, exc, tb):
        if self.channel is not None:
            await self.channel.close()
        if self.connection is not None:
            await self.connection.close()
