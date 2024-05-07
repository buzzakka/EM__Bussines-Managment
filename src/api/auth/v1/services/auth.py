from src.api.auth.utils import exceptions, secret
from src.core.utils import UnitOfWork, BaseService

from src.api.auth.models import CredentialModel, SecretModel
from src.api.auth.schemas import (
    UserLoginSchema,
    TokenSchema,
)


class AuthService(BaseService):

    repository: str = 'account'

    @classmethod
    async def login(cls, uow: UnitOfWork, user: UserLoginSchema) -> TokenSchema:
        async with uow:
            await cls._check_account(uow=uow, email=user.email, password=user.password)

            token: str = await cls._create_and_return_jwt(uow=uow, email=user.email)
            return TokenSchema(access_token=token)

    @classmethod
    async def logout(cls, uow: UnitOfWork, account_id: int):
        async with uow:
            await uow.credential.delete_by_query(account_id=account_id)

    @classmethod
    async def _check_account(cls, uow: UnitOfWork, email: str, password: str):
        account_info: SecretModel = await uow.secret.get_account_info_and_password(email=email)

        if account_info is None or not account_info.is_active:
            raise exceptions.incorrect_email_or_password()

        is_correct_password: bool = secret.validate_password(
            password, account_info.password_hash)

        if not is_correct_password:
            raise exceptions.incorrect_email_or_password()

    @classmethod
    async def _create_and_return_jwt(cls, uow: UnitOfWork, email: str):
        db_payload = await uow.credential.get_payload(email=email)

        if db_payload is None:
            raise exceptions.incorrect_email_or_password()

        payload: dict = secret.make_payload(
            account_id=str(db_payload.account_id),
            company_id=str(db_payload.company_id),
            is_admin=db_payload.is_admin
        )

        token: str = secret.encode_jwt(payload=payload)

        credential_obj: CredentialModel = await uow.credential.get_by_query_one_or_none(
            account_id=payload['account_id']
        )

        if credential_obj is None:
            credential_obj = await uow.credential.add_one_and_get_obj(
                account_id=payload['account_id'],
                api_key=token
            )
        else:
            credential_obj.api_key = token

        return token
