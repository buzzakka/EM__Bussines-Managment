from pydantic import UUID4, BaseModel, EmailStr


class AccountSchema(BaseModel):
    id: UUID4
    email: EmailStr


class UserSchema(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
