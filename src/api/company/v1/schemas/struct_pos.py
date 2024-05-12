from pydantic import BaseModel, UUID4

from src.core.schemas import BaseResponseModel

from src.api.company.schemas import StructPositionSchema


class StructPositionResponseSchema(BaseResponseModel):
    payload: StructPositionSchema


class AddStructPositionRequestSchema(BaseModel):
    struct_id: UUID4
    position_id: UUID4
    member_id: UUID4 | None = None
    is_director: bool


class AddStructPositionResponseSchema(StructPositionResponseSchema):
    ...


class UpdateStructPositionRequestSchema(AddStructPositionRequestSchema):
    struct_position_id: UUID4
    struct_id: UUID4 | None = None
    position_id: UUID4 | None = None
    member_id: UUID4 | None = None
    is_director: bool | None = None


class UpdateStructPositionResponseSchema(StructPositionResponseSchema):
    ...


class DeleteStructPositionResponseSchema(StructPositionResponseSchema):
    ...
