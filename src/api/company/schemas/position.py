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


class AddStructReqeustSchema(BaseModel):
    name: str
    parent_id: UUID4 = None


class DeleteStructRequestSchema(BaseModel):
    struct_id: UUID4


class UpdateStructRequestSchema(BaseModel):
    struct_id: UUID4
    new_name: str


class UpdateStructResponseSchema(BaseModel):
    new_item: UpdateStructRequestSchema
    message: str = 'Объект успешно изменён!'
