from pydantic import BaseModel, EmailStr
from src.core.schemas import BaseResponseModel


class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class UserLoginResponseSchema(BaseResponseModel):
    payload: TokenSchema | None = None
