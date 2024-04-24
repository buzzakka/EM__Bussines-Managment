from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    password: bytes
    first_name: str
    last_name: str
    is_active: bool
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
