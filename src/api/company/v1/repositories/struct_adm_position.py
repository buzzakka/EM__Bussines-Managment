from sqlalchemy import Result, select, UUID

from src.core.utils import SqlAlchemyRepository
from src.api.company.models import StructAdmPositionsModel, PositionModel, MemberModel, StructAdmModel


class StructAdmPositionRepository(SqlAlchemyRepository):
    model = StructAdmPositionsModel

    async def check_struct(self, company_id: UUID, **kwargs):
        query = (
            select(PositionModel, MemberModel, StructAdmModel)
            .join(MemberModel, MemberModel.company_id == PositionModel.company_id)
            .join(StructAdmModel, StructAdmModel.company_id == PositionModel.company_id)
            .filter_by(PositionModel.company_id==company_id, **kwargs)
        )
        res: Result = await self.session.execute(query)
        return res.first()
