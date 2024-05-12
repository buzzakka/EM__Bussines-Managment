from typing import Any
from pydantic import BaseModel, UUID4, field_validator
from datetime import datetime

from src.core.schemas import BaseResponseModel
from src.api.company.models.task import TaskStatus
from src.api.company.schemas import TaskSchema


class AddTaskRequestSchema(BaseModel):
    title: str
    description: str | None = None
    responsible_id: UUID4 | None = None
    deadline: datetime

    observers: list[UUID4] = None
    performers: list[UUID4] = None

    @field_validator('deadline')
    def deadline_validate(cls, v: Any):
        if v < datetime.now():
            raise ValueError('Некоретная дата deadline.')
        return v


class TaskResponseSchema(BaseResponseModel):
    payload: TaskSchema


class AddTaskResponseSchema(TaskResponseSchema):
    ...


class UpdateTaskRequestSchema(AddTaskRequestSchema):
    task_id: UUID4
    title: str = None
    deadline: datetime = None
    status: TaskStatus = None


class UpdateTaskResponseSchema(TaskResponseSchema):
    ...


class DeleteTaskResponseSchema(TaskResponseSchema):
    ...
