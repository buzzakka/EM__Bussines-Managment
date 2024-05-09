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


class PositionDeletePayloadSchema(BaseModel):
    position_id: UUID4
    title: str


class PositionDeleteResponseSchema(BaseResponseModel):
    payload: PositionDeletePayloadSchema | None = None
