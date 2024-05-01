import enum
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    int_pk_T,
    created_at_T,
    updated_at_T
)


class InviteTypes(enum.Enum):
    ACCOUNT: str = 'Account registration'
    EMPLOYMENT: str = 'Employe registration'


class InviteModel(Base):
    __tablename__ = 'invite'

    id: Mapped[int_pk_T]
    email: Mapped[str]
    token: Mapped[str]
    invite_type: Mapped[Enum] = mapped_column(Enum(InviteTypes))
    is_confirmed: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
