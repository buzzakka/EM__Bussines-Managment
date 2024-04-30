from datetime import datetime
from pydantic import BaseModel


class CompanySchema(BaseModel):

    id: int = None
    name: str
    created_at: datetime
    updated_at: datetime


class MemberSchema(BaseModel):

    id: int = None
    account_id: int
    company_id: int
    is_admin: bool
