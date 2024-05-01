from copy import deepcopy
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    int_pk_T,
    created_at_T,
    updated_at_T
)

from src.api.auth.schemas import UserSchema


class UserModel(Base):
    __tablename__ = 'user'

    user_id: Mapped[int_pk_T]

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    first_name: Mapped[str]
    last_name: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self) -> UserSchema:
        dict_copy: dict = deepcopy(self.__dict__)
        dict_copy.pop('_sa_instance_state')
        return UserSchema(**dict_copy)
