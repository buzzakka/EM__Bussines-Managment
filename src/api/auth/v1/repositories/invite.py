from src.core.utils import SqlAlchemyRepository
from src.api.auth.models import InviteModel


class InviteRepository(SqlAlchemyRepository):
    model = InviteModel
