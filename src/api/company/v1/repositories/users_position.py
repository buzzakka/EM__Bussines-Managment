from src.api.company.models import UserPositionModel
from src.core.utils import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = UserPositionModel
