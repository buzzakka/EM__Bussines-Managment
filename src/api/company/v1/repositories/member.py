from sqlalchemy import select, and_

from src.api.auth.models import AccountModel
from src.api.company.models import MemberModel
from src.core.utils import SqlAlchemyRepository


class MemberRepository(SqlAlchemyRepository):
    model = MemberModel

    async def get_account_by_company_id_and_email_or_none(self, company_id: str, email: str) -> AccountModel:
        query = (
            select(AccountModel)
            .join(MemberModel)
            .filter(and_(AccountModel.email == email, MemberModel.company_id == company_id))
        )
        _obj = await self.session.execute(query)
        return _obj.unique().scalar_one_or_none()
        
