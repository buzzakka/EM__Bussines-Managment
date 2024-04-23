from src.api.auth.v1.models.user import UserModel
from src.core.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel
