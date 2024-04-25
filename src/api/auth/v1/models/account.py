from copy import deepcopy
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import int_pk_T
from src.api.auth.v1.schemas import AccountSchema


class AccountModel(Base):
    __tablename__ = 'account'

    id: Mapped[int_pk_T]
    email: Mapped[str] = mapped_column(unique=True)
    status: Mapped[bool] = mapped_column(default=False)
    
    def to_pydantic_schema(self):
        dict_copy: dict = deepcopy(self.__dict__)
        dict_copy.pop('_sa_instance_state')
        return AccountSchema(**dict_copy)