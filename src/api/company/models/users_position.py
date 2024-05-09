from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T
)


class UserPositionModel(Base):
    __tablename__ = 'user_position'

    id: Mapped[uuid_pk_T]
    account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('account.id'))
    possition_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('position.id'))

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
