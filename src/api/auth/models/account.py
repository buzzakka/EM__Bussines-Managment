from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T


class AccountModel(Base):
    __tablename__ = 'account'

    id: Mapped[uuid_pk_T]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=False)

    secret = relationship(
        'SecretModel', back_populates='account', uselist=False
    )
    credential = relationship(
        'CredentialModel', back_populates='account', uselist=False
    )
