from src.api.company.models import MemberModel
from src.core.utils import SqlAlchemyRepository


class MemberRepository(SqlAlchemyRepository):
    model = MemberModel
