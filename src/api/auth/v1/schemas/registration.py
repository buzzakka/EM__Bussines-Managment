from fastapi import status
from pydantic import BaseModel, EmailStr
from typing import Optional

from src.core.schemas import BaseResponseModel

from src.api.auth.schemas.mixins import EmailSchema


class CheckAccountResponseSchema(BaseResponseModel):
    payload: EmailSchema | None = None


class SignUpRequestSchema(BaseModel):
    account: EmailStr
    invite_token: str


class SignUpResponseSchema(BaseResponseModel):
    payload: EmailSchema | None = None


class AccountRegisterPayload(BaseModel):
    account: EmailStr
    first_name: str
    last_name: str
    company_name: str


class AccountRegisterRequestSchema(AccountRegisterPayload):
    password: str


class AccountRegisterResponseSchema(BaseResponseModel):
    payload: AccountRegisterPayload | None = None
