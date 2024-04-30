from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class PayloadSchema(BaseModel):
    account_id: int
    company_id: int
    is_admin: bool
