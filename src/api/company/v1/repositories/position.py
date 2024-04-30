from src.api.company.models import PositionModel
from src.core.utils import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = PositionModel
