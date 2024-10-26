from pydantic import BaseModel


class AccessTorenReponse(BaseModel):
    access_token: str
    token_type: str
