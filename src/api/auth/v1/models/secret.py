from copy import deepcopy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import int_pk_T

from src.api.auth.v1.schemas import SecretSchema


class SecretModel(Base):
    __tablename__ = 'secret'

    id: Mapped[int_pk_T]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    password_hash: Mapped[bytes]

    def to_pydantic_schema(self):
        dict_copy: dict = deepcopy(self.__dict__)
        dict_copy.pop('_sa_instance_state')
        return SecretSchema(**dict_copy)
