from src.core.utils import SqlAlchemyRepository
from src.api.auth.models import UserModel


class UserRepository(SqlAlchemyRepository):
    model = UserModel
