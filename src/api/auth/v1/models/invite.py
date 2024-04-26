from copy import deepcopy
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import int_pk_T, created_at_T

from src.api.auth.v1.schemas import InviteSchema


class InviteModel(Base):
    __tablename__ = 'invite'

    id: Mapped[int_pk_T]
    email: Mapped[str]
    token: Mapped[str]
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at_T]

    def to_pydantic_schema(self):
        dict_copy: dict = deepcopy(self.__dict__)
        dict_copy.pop('_sa_instance_state')
        return InviteSchema(**dict_copy)
