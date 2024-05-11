from sqlalchemy import Result, Select, select
from src.api.company.models import StructAdmModel

from src.core.utils import SqlAlchemyRepository


class StructAdmRepository(SqlAlchemyRepository):
    model = StructAdmModel

    async def add_new_struct(
        self,
        company_id: str, name: str, parent_obj: StructAdmModel | None = None,
    ) -> None:
        struct_obj: StructAdmModel = StructAdmModel(
            company_id=company_id,
            name=name,
            parent=parent_obj
        )
        self.session.add(struct_obj)

        return struct_obj

    async def delete_struct_and_descendants(self, parent_obj: StructAdmModel) -> None:
        query = select(self.model).filter(
            self.model.path.descendant_of(parent_obj.path))

        descendants = await self.session.execute(query)
        descendant_objects = descendants.fetchall()

        for descendant_row in descendant_objects:
            descendant_obj = descendant_row[0]
            await self.session.delete(descendant_obj)

        await self.session.delete(parent_obj)
