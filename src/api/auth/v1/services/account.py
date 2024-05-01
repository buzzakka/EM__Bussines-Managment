from src.core.utils import UnitOfWork, BaseService

from src.api.auth.v1.services.invite import InviteService
from src.api.auth.v1.services.credential import CredentialService
from src.api.auth.models import InviteModel, UserModel
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


class UserService(BaseService):

    repository: str = 'user'

    @classmethod
    async def check_account(cls, uow: UnitOfWork, email: str) -> CheckAccountResponseSchema:
        """Проверка статуса аккаунта с адресом электронной почты email."""
        is_account_exists: bool = await cls.is_account_exists(uow=uow, email=email)

        if is_account_exists:
            raise exceptions.account_already_registered()

        await InviteService.create_invite_token(uow=uow, email=email)

        return CheckAccountResponseSchema(account=email)

    # @classmethod
    # async def sign_up_company(
    #     cls,
    #     uow: UnitOfWork,
    #     sign_up_data: SignUpRequestSchema
    # ) -> SignUpResponseSchema:
    #     email: str = sign_up_data.account
    #     token: str = sign_up_data.invite_token

    #     is_account_exists: bool = await cls.is_account_exists(uow, email)

    #     if is_account_exists:
    #         raise exceptions.account_already_registered()

    #     await InviteService.check_invite_token(uow, email, token)

    #     return SignUpResponseSchema(account=sign_up_data.account)

    # @classmethod
    # async def is_account_exists(
    #     cls,
    #     uow: UnitOfWork,
    #     email: str
    # ) -> bool:
    #     return await cls.get_by_query_one_or_none(uow, email=email) is not None

    # @classmethod
    # async def register_company(
    #     cls,
    #     uow: UnitOfWork,
    #     account: str, password: str, first_name: str, last_name: str, company_name: str,
    # ) -> None:
    #     async with uow:
    #         await cls._get_invite_obj_or_raise(uow=uow, email=account)

    #         await cls._check_if_account_exists_or_raise(uow=uow, email=account)

    #         user_obj: UserModel = await uow.user.add_one_and_get_obj(
    #             first_name=first_name,
    #             last_name=last_name
    #         )

    #         account_obj: AccountModel = await uow.account.add_one_and_get_obj(email=account)

    #         await cls._add_secret_obj(uow=uow, user_obj=user_obj, account_obj=account_obj, password=password)

    #         company_obj: CompanyModel = await uow.company.add_one_and_get_obj(
    #             name=company_name
    #         )

    #         await uow.member.add_one(account_id=account_obj.id, company_id=company_obj.id, is_admin=True)

    #         response_data: SignUpCompleteResponseSchema = SignUpCompleteResponseSchema(
    #             user_id=user_obj.id,
    #             email=account_obj.email,
    #             first_name=user_obj.first_name,
    #             last_name=user_obj.last_name,
    #             company_name=company_obj.name
    #         )

    #         return response_data

    # @classmethod
    # async def sign_up_emloyment_user(
    #     cls,
    #     uow: UnitOfWork,
    #     invite_id: int,
    #     invite_token: str,
    # ):
    #     async with uow:
    #         invite_obj: InviteModel = await uow.invite.get_by_query_one_or_none(
    #             id=invite_id,
    #             token=invite_token,
    #             invite_type='employment',
    #         )
    #         if invite_obj is None:
    #             raise exceptions.page_not_found()

    #         if invite_obj.is_confirmed:
    #             raise exceptions.invite_token_already_confirmed()

    #         invite_obj.is_confirmed = True

    # @classmethod
    # async def register_employment_user(cls, uow: UnitOfWork, email: str, password: str):
    #     await cls._get_invite_obj_or_raise(uow=uow, email=email, invite_type='employment')
        
    #     await cls._check_if_account_exists_or_raise(uow=uow, email=email)

    # @classmethod
    # async def authentication(cls, uow: UnitOfWork, email: str, password: str) -> SecretModel:
    #     async with uow:
    #         account_info: SecretModel = await uow.secret.get_account_info_and_password_or_none(email=email)

    #         if account_info is None or not utils.validate_password(password, account_info.password_hash):
    #             raise exceptions.incorrect_email_or_password()

    #         return account_info

    # @classmethod
    # async def login(cls, uow: UnitOfWork, user: UserLoginSchema) -> TokenSchema:
    #     token = await CredentialService.add_token(uow, user.email)
    #     return TokenSchema(access_token=token, token_type='Bearer')

    # @classmethod
    # async def logout(cls, uow: UnitOfWork, account_id: int):
    #     async with uow:
    #         await uow.credential.delete_by_query(account_id=account_id)

    # @classmethod
    # async def _get_invite_obj_or_raise(
    #     cls,
    #     uow: UnitOfWork,
    #     email: str,
    #     invite_type: str = 'registration'
    # ) -> InviteModel:
    #     invite_info: dict = {
    #         'email': email,
    #         'is_confirmed': True,
    #         'invite_type': invite_type
    #     }
    #     _invite_obj: InviteModel = await uow.invite.get_by_query_one_or_none(**invite_info)

    #     if _invite_obj is None or not _invite_obj.is_confirmed:
    #         raise exceptions.account_is_not_confirmed()

    #     return _invite_obj

    # @classmethod
    # async def _check_if_account_exists_or_raise(cls, uow: UnitOfWork, email: str) -> AccountModel:
    #     is_account_exists: bool = await uow.account.get_by_query_one_or_none(email=email) is not None

    #     if is_account_exists:
    #         raise exceptions.account_already_registered()

    # @classmethod
    # async def _add_secret_obj(
    #     cls,
    #     uow: UnitOfWork,
    #     user_obj: UserModel,
    #     account_obj: AccountModel,
    #     password: str,
    # ) -> None:
    #     secret: dict = {
    #         'user_id': user_obj.id,
    #         'account_id': account_obj.id,
    #         'password_hash': utils.hash_password(password)
    #     }
    #     await uow.secret.add_one(**secret)
