from src.core.utils import SqlAlchemyRepository
from src.api.auth.v1.models import CredentialModel


class CredentialRepository(SqlAlchemyRepository):
    model = CredentialModel
