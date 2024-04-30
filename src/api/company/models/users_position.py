from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    int_pk_T,
    created_at_T,
    updated_at_T
)


class UserPositionModel(Base):
    __tablename__ = 'user_position'

    id: Mapped[int_pk_T]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    possition_id: Mapped[str] = mapped_column(ForeignKey('position.id'))

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
