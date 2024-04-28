from sqlalchemy import select
from sqlalchemy.orm import joinedload


from src.core.utils import SqlAlchemyRepository
from src.api.auth.v1.models import CredentialModel, AccountModel
from src.api.company.v1.models import MemberModel


class CredentialRepository(SqlAlchemyRepository):
    model = CredentialModel
    
    async def get_payload(self, email: str):
        query = (
            select(MemberModel.account_id, MemberModel.company_id, MemberModel.is_admin)
            .join(AccountModel)
            .filter(AccountModel.email == email)
        )
        _obj = await self.session.execute(query)
        return _obj.first()
        
