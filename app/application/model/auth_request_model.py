
from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    username: str
    password: str


class TokenResponseModel(BaseModel):
    access_token: str
    token_type: str = "bearer"