from src.core.utils import SqlAlchemyRepository
from src.api.auth.v1.models import InviteModel


class InviteRepository(SqlAlchemyRepository):
    model = InviteModel
