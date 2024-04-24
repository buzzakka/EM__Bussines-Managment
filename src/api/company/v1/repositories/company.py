from src.api.company.v1.models.company import CompanyModel
from src.core.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel
