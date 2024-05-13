from datetime import datetime
from pydantic import BaseModel, UUID4, EmailStr
from src.api.auth.models import InviteTypes


class InviteSchema(BaseModel):
    id: UUID4
    email: EmailStr
    token: str
    invite_type: InviteTypes
    is_confirmed: bool


class AccountSchema(BaseModel):
    id: UUID4
    email: EmailStr
    is_active: bool


class UserSchema(BaseModel):
    id: UUID4
    first_name: str
    last_name: str


class SecretSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    account_id: UUID4
    password_hash: bytes


class CompanySchema(BaseModel):
    id: UUID4
    name: str


class MemberSchema(BaseModel):
    id: UUID4
    account_id: UUID4
    company_id: UUID4
    is_admin: bool


class PositionSchema(BaseModel):
    id: UUID4
    title: str
    description: str | None = None
    company_id: UUID4


class StructSchema(BaseModel):
    id: UUID4
    company_id: UUID4
    name: str
    path: str | None = None


class StructPositionSchema(BaseModel):
    id: UUID4
    struct_id: UUID4
    position_id: UUID4
    member_id: UUID4
    is_director: bool


class TaskSchema(BaseModel):
    id: UUID4
    title: str
    author_id: UUID4
    deadline: datetime
    status: str

