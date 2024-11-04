import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
)

import settings
from mailing.exceptions import RabbitException


class AMQPMailConnector:

    def __init__(self) -> None:
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractRobustChannel | None = None

    @property
    def channel(self) -> AbstractRobustChannel:
        if self._channel is None:
            raise RabbitException(
                "Please use context manager for AMQPMailConnector helper."
            )
        return self._channel

    async def __aenter__(self):
        if self._connection is None:
            self._connection = await aio_pika.connect_robust(settings.AMQP_URL)
        if self._channel is None:
            self._channel = await self._connection.channel()
        return self

    async def __aexit__(self, ext_type, exc, tb):
        if self._channel is not None and not self._channel.is_closed:
            await self._channel.close()
        if self._connection is not None and not self._connection.is_closed:
            await self._connection.close()
