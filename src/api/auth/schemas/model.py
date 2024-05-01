from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class InviteSchema(BaseModel):
    id: int = None
    email: str
    token: str
    is_confirmed: bool
    created_at: datetime
    invite_type: str


class CredentialSchema(BaseModel):
    id: int = None
    account_id: int
    created_at: datetime
    api_key: str
