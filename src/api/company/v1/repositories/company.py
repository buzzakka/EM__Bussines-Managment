from src.api.company.v1.models import CompanyModel
from src.core.utils import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel
