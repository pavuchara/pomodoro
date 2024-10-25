from fastapi import FastAPI


from core import routes as core_routes
from tasks import routes as task_routes

app = FastAPI()


app.include_router(core_routes.router)
app.include_router(task_routes.router)
