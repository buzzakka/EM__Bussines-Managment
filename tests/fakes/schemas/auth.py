from datetime import datetime
from pydantic import BaseModel, UUID4


class InviteTestSchema(BaseModel):
    id: UUID4
    email: str
    token: str
    is_confirmed: bool
    created_at: datetime = datetime.now()
    invite_type: str


class AccountTestSchema(BaseModel):
    id: UUID4
    email: str
    is_active: bool


class UserTestSchema(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class SecretTestSchema(BaseModel):
    id: UUID4
    user_id: int
    account_id: int
    password_hash: bytes
