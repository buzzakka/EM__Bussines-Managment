from src.api.auth.v1.models.account import AccountModel
from src.core.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = AccountModel
