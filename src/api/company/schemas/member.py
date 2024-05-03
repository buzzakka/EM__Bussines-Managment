from pydantic import BaseModel, EmailStr, UUID4


class AddMemberRequestSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class AddMemberResponseSchema(BaseModel):
    user: AddMemberRequestSchema
    message: str = 'Пользователь успешно создан'


class UpdateUsersEmailByAdminRequestSchema(BaseModel):
    account_id: UUID4
    new_email: EmailStr


class UpdateUsersEmailByAdminResponseSchema(BaseModel):
    new_email: str
    message: str = 'Адрес электронной почты успешно изменён!'
