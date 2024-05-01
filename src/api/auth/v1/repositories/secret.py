from sqlalchemy.orm import joinedload
from sqlalchemy import Result, select

from src.core.utils import SqlAlchemyRepository
from src.api.auth.models import AccountModel, SecretModel


class SecretRepository(SqlAlchemyRepository):
    model = SecretModel

    async def get_account_id_and_password(self, email: str):
        query = (
            select(SecretModel.account_id, SecretModel.password_hash)
            .join(AccountModel)
            .filter(AccountModel.email == email)
        )
        res: Result = await self.session.execute(query)
        return res.first()
