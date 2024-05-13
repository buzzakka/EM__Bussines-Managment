import datetime
import enum
from typing import Optional
from sqlalchemy import ForeignKey, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.company.schemas import TaskSchema

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T, created_at_T, updated_at_T


class TaskStatus(enum.Enum):
    OPEN: str = 'OPEN'
    IN_PROGRESS: str = 'IN_PROGRESS'
    COMPLETED: str = 'COMPLETED'


class TaskModel(Base):
    __tablename__ = 'task'

    id: Mapped[uuid_pk_T]
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(
        nullable=None, default=None
    )
    author_id: Mapped[UUID] = mapped_column(ForeignKey('account.id'))
    responsible_id: Mapped[UUID] = mapped_column(
        ForeignKey('account.id'), nullable=True, default=None
    )
    deadline: Mapped[datetime.datetime]
    status: Mapped[Enum] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.OPEN
    )

    observers: Mapped[list['AccountModel']] = relationship(
        secondary='task_observers', back_populates='observed_tasks'
    )
    performers: Mapped[list['AccountModel']] = relationship(
        secondary='task_performers', back_populates='performed_tasks'
    )

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self):
        return TaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            author_id=self.author_id,
            responsible_id=self.responsible_id,
            deadline=self.deadline,
            status=self.status
        )


class TaskObserversModel(Base):
    __tablename__ = 'task_observers'

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'),
        primary_key=True,
    )
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey('account.id', ondelete='CASCADE'),
        primary_key=True,
    )


class TaskPerformersModel(Base):
    __tablename__ = 'task_performers'

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'),
        primary_key=True,
    )
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey('account.id', ondelete='CASCADE'),
        primary_key=True,
    )
