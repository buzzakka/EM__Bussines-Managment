from datetime import datetime, timezone
from pydantic import BaseModel


class CompanyTestSchema(BaseModel):
    name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class MemberTestSchema(BaseModel):
    account_id: int
    company_id: int
    is_admin: bool
