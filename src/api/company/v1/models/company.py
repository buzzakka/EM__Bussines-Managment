from copy import deepcopy
from sqlalchemy.orm import Mapped

from src.api.company.v1.schemas import CompanySchema
from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    int_pk_T,
    created_at_T,
    updated_at_T
)


class CompanyModel(Base):
    __tablename__ = 'company'

    id: Mapped[int_pk_T]
    name: Mapped[str]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self):
        dict_copy: dict = deepcopy(self.__dict__)
        dict_copy.pop('_sa_instance_state')
        return CompanySchema(**dict_copy)
