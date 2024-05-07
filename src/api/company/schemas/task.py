from typing import Any
from pydantic import BaseModel, UUID4, field_validator
from datetime import datetime

from src.api.company.models.task import TaskStatus


class AddTaskRequestSchema(BaseModel):
    title: str
    description: str = None
    responsible_id: UUID4 = None
    deadline: datetime
    status: TaskStatus = TaskStatus.OPEN
    
    observers: list[UUID4] = None
    performers: list[UUID4] = None
    
    @field_validator('deadline')
    def deadline_validate(cls, v: Any):
        if v < datetime.now():
            raise ValueError('Некоретная дата deadline.')
        return v

# class AddTaskResponseM
