from src.api.company.v1.models import UserPositionModel
from src.core.utils import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = UserPositionModel
