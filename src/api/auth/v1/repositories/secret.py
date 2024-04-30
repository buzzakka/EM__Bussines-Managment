from sqlalchemy import Result, select

from src.core.utils import SqlAlchemyRepository
from src.api.auth.models import AccountModel, SecretModel


class SecretRepository(SqlAlchemyRepository):
    model = SecretModel

    async def get_account_info_and_password_or_none(self, email: str):
        query = (
            select(SecretModel)
            .join(AccountModel, AccountModel.id == SecretModel.account_id)
            .filter(AccountModel.email == email)
        )
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()
