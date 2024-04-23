from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    password: bytes
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
