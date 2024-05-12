from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T

from src.api.auth.schemas import AccountSchema


class AccountModel(Base):
    __tablename__ = 'account'

    id: Mapped[uuid_pk_T]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=False)

    secret = relationship(
        'SecretModel', back_populates='account', uselist=False
    )
    credential = relationship(
        'CredentialModel', back_populates='account', uselist=False
    )

    observed_tasks: Mapped[list['TaskModel']] = relationship(
        secondary='task_observers', back_populates='observers'
    )
    performed_tasks: Mapped[list['TaskModel']] = relationship(
        secondary='task_performers', back_populates='performers'
    )

    def to_pydantic_schema(self):
        return AccountSchema(
            id=self.id,
            email=self.email
        )
