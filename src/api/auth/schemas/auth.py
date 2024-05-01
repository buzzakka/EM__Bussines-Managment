from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
