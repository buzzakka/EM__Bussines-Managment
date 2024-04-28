from copy import deepcopy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins.custom_types import int_pk_T, created_at_T
from src.api.auth.v1.schemas.model import CredentialSchema


class CredentialModel(Base):
    __tablename__ = 'credential'

    id: Mapped[int_pk_T]
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    created_at: Mapped[created_at_T]
    api_key: Mapped[str]

    account: Mapped['AccountModel'] = relationship(lazy='joined')
    
    def to_pydantic_schema(self):
        dict_copy: dict = deepcopy(self.__dict__)
        dict_copy.pop('_sa_instance_state')
        return CredentialSchema(**dict_copy)
