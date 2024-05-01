from sqlalchemy.orm import Mapped, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    int_pk_T,
    created_at_T,
    updated_at_T
)


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int_pk_T]
    first_name: Mapped[str]
    last_name: Mapped[str]

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    secret = relationship('SecretModel', back_populates='user', uselist=False)
