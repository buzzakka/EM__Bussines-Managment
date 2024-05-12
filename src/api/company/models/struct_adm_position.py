from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.api.company.schemas import StructPositionSchema

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

    def to_pydantic_schema(self):
        return StructPositionSchema(
            id=self.id,
            struct_id=self.struct_id,
            position_id=self.position_id,
            member_id=self.member_id,
            is_director=self.is_director
        )
