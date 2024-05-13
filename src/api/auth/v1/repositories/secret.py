from sqlalchemy import Result, select, update

from src.core.utils import SqlAlchemyRepository

from src.api.auth.models import AccountModel, SecretModel


class SecretRepository(SqlAlchemyRepository):
    model = SecretModel

    async def get_account_info_and_password(self, email: str):
        query = (
            select(
                SecretModel.account_id,
                SecretModel.password_hash,
                AccountModel.is_active
            )
            .join(AccountModel)
            .filter(AccountModel.email == email)
        )
        res: Result = await self.session.execute(query)
        return res.first()

    async def change_password(self, account_id: str, new_password: bytes):
        stmt = (
            update(self.model)
            .where(account_id == account_id)
            .values(password_hash=new_password)
        )
        await self.session.execute(stmt)
