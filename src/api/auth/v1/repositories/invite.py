from src.api.auth.v1.models.invite import InviteModel
from src.core.utils.repository import SqlAlchemyRepository


class InviteRepository(SqlAlchemyRepository):
    model = InviteModel
