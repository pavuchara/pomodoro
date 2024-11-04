from contextlib import asynccontextmanager

from fastapi import FastAPI

from mailing.consumers import make_amqp_consumers


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection, channel = await make_amqp_consumers()
    try:
        yield
    finally:
        await connection.close()
        await channel.close()


app = FastAPI(lifespan=lifespan)
