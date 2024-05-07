from pydantic import BaseModel
from src.core.schemas import BaseResponseModel


class UserLoginRequestSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class UserLoginResponseSchema(BaseResponseModel):
    payload: TokenSchema | None = None
