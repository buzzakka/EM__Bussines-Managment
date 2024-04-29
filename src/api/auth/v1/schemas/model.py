from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class SecretSchema(BaseModel):
    id: int
    user_id: int
    account_id: int
    password_hash: bytes


class InviteSchema(BaseModel):
    id: int = None
    email: str
    token: str
    is_confirmed: bool
    created_at: datetime
    invite_type: str


class AccountSchema(BaseModel):
    id: int
    email: str
    is_active: bool


class CredentialSchema(BaseModel):
    id: int
    account_id: int
    created_at: datetime
    api_key: str
