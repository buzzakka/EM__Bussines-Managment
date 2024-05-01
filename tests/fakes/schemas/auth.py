from datetime import datetime, timezone
from pydantic import BaseModel


class InviteTestSchema(BaseModel):
    email: str
    token: str
    is_confirmed: bool
    created_at: datetime = datetime.now()
    invite_type: str


class AccountTestSchema(BaseModel):
    email: str
    is_active: bool


class UserTestSchema(BaseModel):
    first_name: str
    last_name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class SecretTestSchema(BaseModel):
    user_id: int
    account_id: int
    password_hash: bytes
