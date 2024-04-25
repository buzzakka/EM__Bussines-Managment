from src.core.utils import SqlAlchemyRepository
from src.api.auth.v1.models import UserModel


class UserRepository(SqlAlchemyRepository):
    model = UserModel
