from sqlalchemy import Result, select

from src.core.utils import SqlAlchemyRepository
from src.api.auth.v1.models import AccountModel, SecretModel


class SecretRepository(SqlAlchemyRepository):
    model = SecretModel
    
    async def get_password_by_email_or_none(self, email: str):
        query = (
            select(SecretModel.password_hash)
            .join(AccountModel, SecretModel.account_id == AccountModel.id)
            .filter(AccountModel.email==email)
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()
