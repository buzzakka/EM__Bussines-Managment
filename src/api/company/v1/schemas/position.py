from pydantic import BaseModel, UUID4

from src.core.schemas import BaseResponseModel


class AddPositionRequestSchema(BaseModel):
    title: str
    description: str | None = None


class AddPositionPayloadSchema(AddPositionRequestSchema):
    position_id: UUID4


class AddPositionResponseSchema(BaseResponseModel):
    payload: AddPositionPayloadSchema
