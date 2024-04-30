from src.core.utils import UnitOfWork, BaseService

from src.api.auth.v1.services.invite import InviteService
from src.api.auth.v1.services.credential import CredentialService
from src.api.auth.models import InviteModel, UserModel, AccountModel, SecretModel
from src.api.company.models import CompanyModel
from src.api.auth.schemas import (
    SignUpCompleteResponseSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
    CheckAccountResponseSchema,
    UserLoginSchema,
    TokenSchema,
)
from src.api.auth import exceptions
from src.api.auth import utils


class AccountService(BaseService):

    repository: str = 'account'

    @classmethod
    async def check_account(cls, uow: UnitOfWork, email: str) -> CheckAccountResponseSchema:
        """Проверка статуса аккаунта с адресом электронной почты email."""
        is_account_exists: bool = await cls.is_account_exists(uow=uow, email=email)

        if is_account_exists:
            raise exceptions.account_already_registered()

        await InviteService.create_invite_token(uow=uow, email=email)

        return CheckAccountResponseSchema(account=email)

    @classmethod
    async def sign_up(
        cls,
        uow: UnitOfWork,
        sign_up_data: SignUpRequestSchema
    ) -> SignUpResponseSchema:
        email: str = sign_up_data.account
        token: str = sign_up_data.invite_token

        is_account_exists: bool = await cls.is_account_exists(uow, email)

        if is_account_exists:
            raise exceptions.account_already_registered()

        await InviteService.check_invite_token(uow, email, token)

        return SignUpResponseSchema(account=sign_up_data.account)

    @classmethod
    async def is_account_exists(
        cls,
        uow: UnitOfWork,
        email: str
    ) -> bool:
        return await cls.get_by_query_one_or_none(uow, email=email) is not None

    @classmethod
    async def register_company(
        cls,
        uow: UnitOfWork,
        user_data: dict
    ) -> None:
        async with uow:
            invite_info: dict = cls._generate_invite_info(user_data)
            _invite: InviteModel = await uow.invite.get_by_query_one_or_none(**invite_info)

            if _invite is None or not _invite.is_confirmed:
                raise exceptions.account_is_not_confirmed()

            is_account_exists: bool = await uow.account.get_by_query_one_or_none(email=user_data.get('account')) is not None

            if is_account_exists:
                raise exceptions.account_already_registered()

            user_info: dict = cls._generate_user_info(user_data)
            user_obj: UserModel = await uow.user.add_one_and_get_obj(**user_info)

            account_obj: AccountModel = await uow.account.add_one_and_get_obj(email=user_data.get('account'))

            secret_info: dict = cls._generate_secret_info(
                user_obj, account_obj, user_data.get('password'))
            await uow.secret.add_one(**secret_info)

            company_obj: CompanyModel = await uow.company.add_one_and_get_obj(name=user_data.get('company_name'))
            
            await uow.member.add_one(account_id=account_obj.id, company_id=company_obj.id, is_admin=True)

            response_data: SignUpCompleteResponseSchema = SignUpCompleteResponseSchema(
                user_id=user_obj.id,
                email=account_obj.email,
                first_name=user_obj.first_name,
                last_name=user_obj.last_name,
                company_name=company_obj.name
            )

            return response_data

    @classmethod
    async def authentication(cls, uow: UnitOfWork, email: str, password: str) -> SecretModel:
        async with uow:
            account_info: SecretModel = await uow.secret.get_account_info_and_password_or_none(email=email)

            if account_info is None or not utils.validate_password(password, account_info.password_hash):
                raise exceptions.incorrect_email_or_password()

            return account_info

    @classmethod
    async def login(cls, uow: UnitOfWork, user: UserLoginSchema) -> TokenSchema:
        token = await CredentialService.add_token(uow, user.email)
        return TokenSchema(access_token=token, token_type='Bearer')

    @classmethod
    async def logout(cls, uow: UnitOfWork, account_id: int):
        async with uow:
            await uow.credential.delete_by_query(account_id=account_id)

    @classmethod
    def _generate_invite_info(cls, user_data: dict) -> dict:
        return {
            'email': user_data.get('account'),
            'is_confirmed': True
        }

    @classmethod
    def _generate_user_info(cls, user_data: dict) -> dict:
        return {
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
        }

    @classmethod
    def _generate_secret_info(
        cls,
        user_obj: UserModel,
        account_obj: AccountModel,
        password: str
    ) -> dict:
        return {
            'user_id': user_obj.id,
            'account_id': account_obj.id,
            'password_hash': utils.hash_password(password)
        }
