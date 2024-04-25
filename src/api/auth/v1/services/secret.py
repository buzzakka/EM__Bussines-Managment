from src.core.utils import UnitOfWork, BaseService


class SecretService(BaseService):
    repository = 'secret'
    
    @classmethod
    async def get_password_by_email(cls, uow: UnitOfWork, email: str):
        async with uow:
            hashed_password: bytes = await uow.secret.get_password_by_email_or_none(email)
            return hashed_password
