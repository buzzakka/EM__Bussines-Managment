from datetime import datetime
from pydantic import BaseModel


class InviteSchema(BaseModel):
    id: int
    email: str
    token: str
    is_confirmed: bool
    created_at: datetime
