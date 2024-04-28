from src.api.company.v1.models import PositionModel
from src.core.utils import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = PositionModel
