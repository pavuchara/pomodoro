from pydantic import BaseModel


class MailCallbackHandlerSchema(BaseModel):
    task: str
    status: bool
    message: str
