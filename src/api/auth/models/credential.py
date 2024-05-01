from copy import deepcopy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins.custom_types import int_pk_T, created_at_T
from src.api.auth.schemas.model import CredentialSchema


class CredentialModel(Base):
    __tablename__ = 'credential'

    id: Mapped[int_pk_T]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    created_at: Mapped[created_at_T]
    api_key: Mapped[str]

    user: Mapped['UserModel'] = relationship(lazy='joined')
