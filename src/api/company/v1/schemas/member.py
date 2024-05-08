from pydantic import UUID4, BaseModel, EmailStr

from src.core.schemas import BaseResponseModel
from src.api.auth.schemas.mixins import EmailSchema


class AddMemberRequestSchema(EmailSchema):
    first_name: str
    last_name: str


class AddMemberResponseSchema(BaseResponseModel):
    payload: AddMemberRequestSchema | None = None


class UpdateUsersEmailByAdminRequestSchema(BaseModel):
    account_id: UUID4
    new_email: EmailStr


class UpdateUsersEmailByAdminResponseSchema(BaseResponseModel):
    payload: UpdateUsersEmailByAdminRequestSchema | None = None


class UpdateUsersNameByAdminRequestSchema(BaseModel):
    account_id: UUID4
    first_name: str
    last_name: str


class UpdateUsersNameByAdminResponseSchema(BaseResponseModel):
    payload: UpdateUsersNameByAdminRequestSchema | None = None
