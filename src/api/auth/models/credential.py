from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins.custom_types import uuid_pk_T, created_at_T


class CredentialModel(Base):
    __tablename__ = 'credential'

    id: Mapped[uuid_pk_T]
    account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('account.id'), unique=True)
    created_at: Mapped[created_at_T]
    api_key: Mapped[str]

    account: Mapped['AccountModel'] = relationship(
        back_populates='credential', uselist=False, lazy='joined'
    )
