from pydantic import BaseModel, UUID4

from src.core.schemas import BaseResponseModel


class AddPositionRequestSchema(BaseModel):
    title: str
    description: str | None = None


class AddPositionPayloadSchema(AddPositionRequestSchema):
    position_id: UUID4


class AddPositionResponseSchema(BaseResponseModel):
    payload: AddPositionPayloadSchema


class UpdatePositionRequestSchema(BaseModel):
    position_id: UUID4
    new_position: AddPositionRequestSchema


class UpdatePositionResponseSchema(BaseResponseModel):
    payload: UpdatePositionRequestSchema | None = None


class DeletePositionPayloadSchema(BaseModel):
    position_id: UUID4
    title: str


class DeletePositionResponseSchema(BaseResponseModel):
    payload: DeletePositionPayloadSchema | None = None


class AddStructRequestSchema(BaseModel):
    name: str
    parent_id: UUID4 | None = None


class AddStructPayloadSchema(BaseModel):
    struct_id: UUID4
    name: str


class AddStructResponseSchema(BaseResponseModel):
    payload: AddStructPayloadSchema | None = None


class UpdateStructRequestSchema(BaseModel):
    struct_id: UUID4
    name: str


class UpdateStructResponseSchema(BaseResponseModel):
    payload: UpdateStructRequestSchema | None = None


class DeleteStructResponseSchema(UpdateStructResponseSchema): ...


class AddStructPositionRequestSchema(BaseModel):
    struct_id: UUID4
    position_id: UUID4
    member_id: UUID4 | None = None
    is_director: bool


class AddStructPositionPayloadSchema(AddStructPositionRequestSchema):
    struct_position_id: UUID4


class AddStructPositionResponseSchema(BaseResponseModel):
    payload: AddStructPositionPayloadSchema | None = None
