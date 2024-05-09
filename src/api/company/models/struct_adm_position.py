from sqlalchemy import ForeignKey, Column, Index, func, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

from src.core.models import Base
from src.core.models.mixins.custom_types import uuid_pk_T, created_at_T, updated_at_T


class StructAdmPositionsModel(Base):
    __tablename__ = 'struct_adm_position'

    id: Mapped[uuid_pk_T]
    struct_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('struct_adm.id', ondelete='CASCADE')
    )
    position_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('position.id', ondelete='CASCADE')
    )
    member_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('member.id', ondelete='SET NULL'), nullable=True, default=None
    )
    is_director: Mapped[bool]

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
