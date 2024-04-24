from datetime import datetime
from pydantic import BaseModel


class InviteSchema(BaseModel):
    id: int
    email: str
    token: str
    status: bool
    created_at: datetime
