from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.company.schemas import PositionSchema

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T
)


class PositionModel(Base):
    __tablename__ = 'position'

    id: Mapped[uuid_pk_T]
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE')
    )

    company: Mapped['CompanyModel'] = relationship(uselist=False)

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self):
        return PositionSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            company_id=self.company_id
        )
