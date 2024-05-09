from sqlalchemy import ForeignKey, Column, Index, func, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

from uuid import uuid4

from src.core.models.base import Base
from src.core.models.mixins.custom_types import uuid_pk_T, created_at_T, updated_at_T


class StructAdmModel(Base):
    __tablename__ = 'struct_adm'

    id: Mapped[uuid_pk_T]
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE')
    )
    name: Mapped[str]
    path = Column(LtreeType, nullable=False)

    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    company: Mapped['CompanyModel'] = relationship(uselist=False)
    parent = relationship(
        'StructAdmModel',
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref='children',
        viewonly=True
    )

    __table_args__ = (
        Index('ix_struct_path', path, postgresql_using='gist'),
    )

    def __init__(self, company_id: str, name: str, parent: 'StructAdmModel' = None):
        self.id = uuid4()
        self.company_id = company_id
        self.name = name

        ltree_id = Ltree(str(self.id).replace('-', '_'))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Struct({self.name=}, {self.company_id=})'
