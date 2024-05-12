from sqlalchemy.orm import Mapped

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T
)

from src.api.company.schemas import CompanySchema


class CompanyModel(Base):
    __tablename__ = 'company'

    id: Mapped[uuid_pk_T]
    name: Mapped[str]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self):
        return CompanySchema(
            id=self.id,
            name=self.name
        )
