from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T

from src.api.company.schemas import MemberSchema


class MemberModel(Base):
    __tablename__ = 'member'

    id: Mapped[uuid_pk_T]
    account_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('account.id', ondelete='CASCADE')
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE')
    )
    is_admin: Mapped[bool] = mapped_column(default=False)

    account: Mapped['AccountModel'] = relationship(uselist=False)
    company: Mapped['CompanyModel'] = relationship(uselist=False)

    def to_pydantic_schema(self):
        return MemberSchema(
            id=self.id,
            account_id=self.account_id,
            company_id=self.company_id,
            is_admin=self.is_admin
        )
