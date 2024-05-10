from sqlalchemy import Result, select, UUID

from src.core.utils import SqlAlchemyRepository
from src.api.company.models import StructAdmPositionsModel, StructAdmModel


class StructAdmPositionRepository(SqlAlchemyRepository):
    model = StructAdmPositionsModel

    async def check_struct_pos_by_company_id(self, struct_pos_id: UUID, company_id: UUID):
        query = (
            select(self.model)
            .join(StructAdmModel, self.model.struct_id == StructAdmModel.id)
            .filter(self.model.id == struct_pos_id, StructAdmModel.company_id == company_id)
        )
        obj: Result = await self.session.execute(query)
        return obj.scalar_one_or_none()
