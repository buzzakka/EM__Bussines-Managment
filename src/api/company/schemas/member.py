from pydantic import BaseModel, EmailStr


class AddMemberRequestSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class AddMemberResponseSchema(BaseModel):
    user: AddMemberRequestSchema
    message: str = 'Пользователь успешно создан'
