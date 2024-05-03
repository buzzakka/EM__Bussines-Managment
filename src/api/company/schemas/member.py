from pydantic import BaseModel, EmailStr


class AddMemberRequestSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class AddMemberResponseSchema(BaseModel):
    user: AddMemberRequestSchema
    message: str = 'Пользователь успешно создан'


class UpdateUsersEmailByAdminRequestSchema(BaseModel):
    email: EmailStr
    new_email: EmailStr


class UpdateUsersEmailByAdminResponseSchema(BaseModel):
    new_email: str
    message: str = 'Адрес электронной почты успешно изменён!'
