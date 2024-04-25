from src.core.utils import SqlAlchemyRepository
from src.api.auth.v1.models import AccountModel


class AccountRepository(SqlAlchemyRepository):
    model = AccountModel
