from pydantic import BaseModel, UUID4

from src.core.schemas import BaseResponseModel

from src.api.company.schemas import StructSchema


class StructResponseSchema(BaseResponseModel):
    payload: StructSchema


class AddStructRequestSchema(BaseModel):
    name: str
    parent_id: UUID4 | None = None


class AddStructResponseSchema(StructResponseSchema):
    ...


class UpdateStructRequestSchema(BaseModel):
    struct_id: UUID4
    name: str


class UpdateStructResponseSchema(StructResponseSchema):
    ...


class DeleteStructResponseSchema(StructResponseSchema):
    ...
