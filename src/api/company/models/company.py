from sqlalchemy.orm import Mapped

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    uuid_pk_T,
    created_at_T,
    updated_at_T
)


class CompanyModel(Base):
    __tablename__ = 'company'

    id: Mapped[uuid_pk_T]
    name: Mapped[str]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]
