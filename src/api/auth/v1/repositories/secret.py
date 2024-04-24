from src.api.auth.v1.models.secret import SecretModel
from src.core.utils.repository import SqlAlchemyRepository


class SecretRepository(SqlAlchemyRepository):
    model = SecretModel
