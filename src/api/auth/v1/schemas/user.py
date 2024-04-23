from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
