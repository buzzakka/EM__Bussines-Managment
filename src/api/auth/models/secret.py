from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T


class SecretModel(Base):
    __tablename__ = 'secret'

    id: Mapped[uuid_pk_T]
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), unique=True)
    account_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('account.id'), unique=True
    )
    password_hash: Mapped[bytes]

    account: Mapped['AccountModel'] = relationship(
        uselist=False, back_populates='secret'
    )
    user: Mapped['UserModel'] = relationship(
        uselist=False, back_populates='secret'
    )
