from sqlalchemy import select


from src.core.utils import SqlAlchemyRepository

from src.api.auth.models import CredentialModel, AccountModel
from src.api.company.models import MemberModel


class CredentialRepository(SqlAlchemyRepository):
    model = CredentialModel

    async def get_payload(self, email: str):
        query = (
            select(
                MemberModel.account_id,
                MemberModel.company_id,
                MemberModel.is_admin
            )
            .join(AccountModel)
            .filter(AccountModel.email == email)
        )
        _obj = await self.session.execute(query)
        return _obj.first()
