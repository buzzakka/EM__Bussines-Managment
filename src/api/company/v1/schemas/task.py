from typing import Any
from pydantic import BaseModel, UUID4, field_validator
from datetime import datetime

from src.core.schemas import BaseResponseModel
from src.api.company.models.task import TaskStatus


class AddTaskRequestSchema(BaseModel):
    title: str
    description: str = None
    responsible_id: UUID4 | None = None
    deadline: datetime
    status: TaskStatus = TaskStatus.OPEN
    
    observers: list[UUID4] | None = None
    performers: list[UUID4] | None = None
    
    @field_validator('deadline')
    def deadline_validate(cls, v: Any):
        if v < datetime.now():
            raise ValueError('Некоретная дата deadline.')
        return v


class AddTaskPayloadSchema(AddTaskRequestSchema):
    task_id: UUID4


class AddTaskResponseSchema(BaseResponseModel):
    payload: AddTaskPayloadSchema | None = None
