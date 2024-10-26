from fastapi import FastAPI

from auth import routes as auth_routes
from core import routes as core_routes
from tasks import routes as task_routes
from user import routes as user_routes

app = FastAPI()


app.include_router(auth_routes.router)
app.include_router(core_routes.router)
app.include_router(task_routes.router)
app.include_router(user_routes.router)
