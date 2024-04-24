from src.core.utils.unit_of_work import UnitOfWork
from src.core.utils.service import BaseService


class AccountService(BaseService):
    repository: str = 'account'
    
    @classmethod
    async def is_account_exists(
        cls,
        uow: UnitOfWork,
        email: str
    ) -> bool:
        return await uow.account.get_by_query_one_or_none(email=email) is not None
