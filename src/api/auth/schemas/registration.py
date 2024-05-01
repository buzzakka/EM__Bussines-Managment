from pydantic import BaseModel, EmailStr


class CheckAccountResponseSchema(BaseModel):
    account: EmailStr
    status: str = 'success'


class SignUpRequestSchema(BaseModel):
    account: EmailStr
    invite_token: str


class SignUpResponseSchema(BaseModel):
    account: EmailStr
    is_confirmed: bool = True


class SignUpCompleteRequestSchema(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class SignUpCompleteResponseSchema(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    company_name: str


class SignUpCompleteEmploymentRequestSchema(BaseModel):
    email: str
    password: str
