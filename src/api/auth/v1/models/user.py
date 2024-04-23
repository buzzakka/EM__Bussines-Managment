from sqlalchemy.orm import Mapped, mapped_column

from src.api.auth.v1.schemas.user import UserSchema
from src.core.models.base import Base
from src.core.models.mixins.custom_types import (
    int_pk_T,
    created_at_T,
    updated_at_T
)


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int_pk_T]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self):
        return UserSchema(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name
        )
