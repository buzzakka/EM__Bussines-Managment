from pydantic import BaseModel, UUID4


class AddPositionRequestSchema(BaseModel):
    title: str
    description: str | None = None


class AddPositionResponseSchema(BaseModel):
    position: AddPositionRequestSchema
    message: str = 'Новая должность добавлена!'


class UpdatePositionRequestSchema(BaseModel):
    position_id: UUID4
    new_position: AddPositionRequestSchema


class UpdatePositionResponseSchema(AddPositionResponseSchema):
    message: str = 'Должность обновлена!'
