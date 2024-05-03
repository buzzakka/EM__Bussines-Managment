from pydantic import BaseModel, EmailStr, UUID4


class CheckAccountResponseSchema(BaseModel):
    email: EmailStr
    message: str = 'Адрес электронной почты свободен.'


class SignUpRequestSchema(BaseModel):
    account: EmailStr
    invite_token: str


class SignUpResponseSchema(CheckAccountResponseSchema):
    message: str = 'Адрес электронной почты успешно подтвержден.'


class SignUpCompleteRequestSchema(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class SignUpCompleteResponseSchema(BaseModel):
    user_id: UUID4
    email: EmailStr
    first_name: str
    last_name: str
    company_name: str


class SignUpCompleteEmploymeeRequestSchema(BaseModel):
    email: str
    password: str


class SignUpCompleteEmployeeResponseSchema(BaseModel):
    account_id: UUID4
    email: EmailStr
