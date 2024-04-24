from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: int
    email: str
    status: str
