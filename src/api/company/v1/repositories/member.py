from sqlalchemy import select, and_

from src.api.auth.models import AccountModel, UserModel, SecretModel
from src.api.company.models import MemberModel, CompanyModel
from src.core.utils import SqlAlchemyRepository


class MemberRepository(SqlAlchemyRepository):
    model = MemberModel

    async def get_account_by_company_id_and_account_id_or_none(self, company_id: str, account_id: str) -> AccountModel:
        query = (
            select(AccountModel)
            .join(MemberModel)
            .filter(and_(AccountModel.id == account_id, MemberModel.company_id == company_id))
        )
        _obj = await self.session.execute(query)
        return _obj.unique().scalar_one_or_none()
    
    async def get_user_by_company_id_and_account_id_or_none(self, company_id: str, account_id: str) -> UserModel:
        query = (
            select(UserModel)
            .join(SecretModel)
            .join(AccountModel)
            .join(MemberModel)
            .filter(and_(AccountModel.id == account_id, MemberModel.company_id == company_id))
        )
        _obj = await self.session.execute(query)
        return _obj.unique().scalar_one_or_none()
