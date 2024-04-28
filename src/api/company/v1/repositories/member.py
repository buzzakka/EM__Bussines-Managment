from src.api.company.v1.models import MemberModel
from src.core.utils import SqlAlchemyRepository


class MemberRepository(SqlAlchemyRepository):
    model = MemberModel
