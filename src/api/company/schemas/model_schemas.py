from datetime import datetime
from pydantic import UUID4, BaseModel


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
    description: str
    company_id: UUID4


class StructSchema(BaseModel):
    id: UUID4
    company_id: UUID4
    name: str
    path: str


class StructPositionSchema(BaseModel):
    id: UUID4
    struct_id: UUID4
    position_id: UUID4
    member_id: UUID4
    is_director: bool


class TaskSchema(BaseModel):
    id: UUID4
    title: str
    description: str | None
    author_id: UUID4
    responsible_id: UUID4 | None
    deadline: datetime
    status: str
