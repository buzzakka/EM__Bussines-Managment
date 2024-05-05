from src.api.company.models import StructAdmModel

from src.core.utils import SqlAlchemyRepository


class StructAdmRepository(SqlAlchemyRepository):
    model = StructAdmModel

    async def add_new_struct(
        company_id: str, name: str,
        parent_obj: StructAdmModel | None = None,
    ):
        struct_obj: StructAdmModel = StructAdmModel(
            company_id=company_id,
            name=name,
            parent=parent_obj
        )
        return struct_obj
