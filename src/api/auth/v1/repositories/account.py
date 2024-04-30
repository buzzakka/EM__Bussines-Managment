from src.core.utils import SqlAlchemyRepository
from src.api.auth.models import AccountModel


class AccountRepository(SqlAlchemyRepository):
    model = AccountModel
