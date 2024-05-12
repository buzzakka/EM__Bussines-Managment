from pydantic import BaseModel, UUID4

from src.core.schemas import BaseResponseModel

from src.api.company.schemas import PositionSchema


class PositionResponseSchema(BaseResponseModel):
    payload: PositionSchema | None = None


class AddPositionRequestSchema(BaseModel):
    title: str
    description: str | None = None


class AddPositionResponseSchema(PositionResponseSchema):
    ...


class UpdatePositionRequestSchema(BaseModel):
    position_id: UUID4
    new_position: AddPositionRequestSchema


class UpdatePositionResponseSchema(PositionResponseSchema):
    ...


class DeletePositionResponseSchema(PositionResponseSchema):
    ...
