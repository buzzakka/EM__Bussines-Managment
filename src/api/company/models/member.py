from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T


class MemberModel(Base):
    __tablename__ = 'member'

    id: Mapped[uuid_pk_T]
    account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('account.id'))
    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('company.id'))
    is_admin: Mapped[bool] = mapped_column(default=False)

    account: Mapped['AccountModel'] = relationship()
    company: Mapped['CompanyModel'] = relationship()
