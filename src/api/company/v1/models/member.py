from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins.custom_types import int_pk_T


class MemberModel(Base):
    __tablename__ = 'member'

    id: Mapped[int_pk_T]
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'))
    company_id: Mapped[int] = mapped_column(ForeignKey('company.id'))
    is_admin: Mapped[bool] = mapped_column(default=False)

    user: Mapped['UserModel'] = relationship()
    company: Mapped['CompanyModel'] = relationship()
