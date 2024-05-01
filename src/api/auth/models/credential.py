from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins.custom_types import int_pk_T, created_at_T


class CredentialModel(Base):
    __tablename__ = 'credential'

    id: Mapped[int_pk_T]
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    created_at: Mapped[created_at_T]
    api_key: Mapped[str]

    account: Mapped['AccountModel'] = relationship(
        back_populates='credential', uselist=False, lazy='joined'
    )
