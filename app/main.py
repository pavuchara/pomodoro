from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth import routes as auth_routes
from core import routes as core_routes
from tasks import routes as task_routes
from user import routes as user_routes

from services.amqp_consumer import make_amqp_consumers


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection, channel = await make_amqp_consumers()
    try:
        yield
    finally:
        await channel.close()
        await connection.close()


app = FastAPI(
    root_path="/api",
    lifespan=lifespan,
)


app.include_router(auth_routes.router)
app.include_router(core_routes.router)
app.include_router(task_routes.router)
app.include_router(user_routes.router)
