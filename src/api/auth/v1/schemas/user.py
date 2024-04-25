from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime


class SignUpRequestSchema(BaseModel):
    account: EmailStr
    invite_token: str


class SignUpCompleteRequestSchema(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
