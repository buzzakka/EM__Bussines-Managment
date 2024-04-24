from sqlalchemy.orm import Mapped

from src.core.models.base import Base
from src.core.models.mixins.custom_types import int_pk_T


class CompanyModel(Base):
    __tablename__ = 'company'
    
    id: Mapped[int_pk_T]
    name: Mapped[str]
