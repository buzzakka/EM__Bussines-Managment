from src.api.company.models import CompanyModel
from src.core.utils import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel
