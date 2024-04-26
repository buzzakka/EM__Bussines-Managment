from src.core.utils import UnitOfWork

from src.api.auth.v1.utils import validate_password
from src.api.auth.exceptions import incorrect_email_or_password
from src.api.auth.v1.models import SecretModel


class AuthService:

    @classmethod
    async def authentication(cls, uow: UnitOfWork, email: str, password: str) -> SecretModel:
        async with uow:
            account_info: SecretModel = await uow.secret.get_account_info_and_password_or_none(email=email)

            password_hash: bytes = account_info.password_hash

            if account_info is None or not validate_password(password, password_hash):
                raise incorrect_email_or_password()

            return account_info
