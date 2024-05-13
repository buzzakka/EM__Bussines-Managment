from pydantic import BaseModel, UUID4, field_validator
from datetime import datetime, timezone

from src.core.schemas import BaseResponseModel
from src.api.company.models.task import TaskStatus
from src.api.company.schemas import TaskSchema


class AddTaskRequestSchema(BaseModel):
    title: str
    description: str | None = None
    responsible_id: UUID4 | None = None
    deadline: datetime

    observers: list[UUID4] | None = None
    performers: list[UUID4] | None = None

    @field_validator('deadline', mode='after')
    @classmethod
    def deadline_validate(cls, v: datetime):
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            v = v.replace(tzinfo=timezone.utc)

        if v < datetime.now(timezone.utc):
            raise ValueError("The deadline must be in the future.")
        v = v.replace(tzinfo=None)
        return v


class TaskPayloadSchema(TaskSchema):
    observers: list[UUID4]
    performers: list[UUID4]


class TaskResponseSchema(BaseResponseModel):
    payload: TaskPayloadSchema


class AddTaskResponseSchema(TaskResponseSchema):
    ...


class UpdateTaskRequestSchema(AddTaskRequestSchema):
    task_id: UUID4
    title: str | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = None


class UpdateTaskResponseSchema(TaskResponseSchema):
    ...


class DeleteTaskResponseSchema(TaskResponseSchema):
    ...
