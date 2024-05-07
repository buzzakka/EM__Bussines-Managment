from random import randint

from src.core.utils import UnitOfWork, BaseService
from src.celery_app.tasks import send_invite_token

from src.api.auth.models import InviteModel, UserModel, AccountModel, SecretModel
from src.api.company.models import CompanyModel
from src.api.auth.schemas import (
    SignUpCompleteResponseSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
    CheckAccountResponseSchema,
    SignUpCompleteEmployeeResponseSchema,
)
from src.api.auth.v1.schemas import (
    CheckAccountResponseSchema,
)
from src.api.auth.v1.utils.exception_responses import (
    account_doesnt_exists_response,
)
from src.api.auth.schemas.mixins import EmailSchema

from src.api.auth.models.invite import InviteTypes
from src.core import exceptions
from src.api.auth import utils


class RegisterService(BaseService):

    repository: str = 'account'

    @classmethod
    async def check_account(cls, uow: UnitOfWork, email: str) -> CheckAccountResponseSchema:
        """Проверка статуса аккаунта с адресом электронной почты email."""
        async with uow:
            is_account_exists: bool = await uow.account.get_by_query_one_or_none(email=email)

            if is_account_exists:
                return account_doesnt_exists_response(email=email)

            invite_obj: InviteModel = await cls._create_invite_token(
                uow=uow,
                email=email,
                invite_type=InviteTypes.ACCOUNT
            )

            send_invite_token.delay(
                to_email=email, invite_token=invite_obj.token
            )

            return CheckAccountResponseSchema(payload=EmailSchema(email=email))

    @classmethod
    async def sign_up_company(
        cls,
        uow: UnitOfWork,
        sign_up_data: SignUpRequestSchema
    ) -> SignUpResponseSchema:
        async with uow:
            email: str = sign_up_data.account
            token: str = sign_up_data.invite_token

            is_account_exists: bool = await cls._is_account_exists(uow=uow, email=email)
            if is_account_exists:
                raise exceptions.account_already_registered()

            await cls._confirm_invite_token(uow=uow, email=email, invite_token=token)

            return SignUpResponseSchema(email=sign_up_data.account)

    @classmethod
    async def register_company(
        cls,
        uow: UnitOfWork,
        account: str, password: str, first_name: str, last_name: str, company_name: str,
    ) -> SignUpCompleteResponseSchema:
        async with uow:
            await cls._get_confirmed_invite_obj_or_raise(uow=uow, email=account, invite_type=InviteTypes.ACCOUNT)

            await cls._check_if_account_exists_or_raise(uow=uow, email=account)

            user_obj: UserModel = await uow.user.add_one_and_get_obj(
                first_name=first_name,
                last_name=last_name
            )

            account_obj: AccountModel = await uow.account.add_one_and_get_obj(email=account)
            account_obj.is_active = True

            await cls._add_secret_obj(uow=uow, user_obj=user_obj, account_obj=account_obj, password=password)

            company_obj: CompanyModel = await uow.company.add_one_and_get_obj(
                name=company_name
            )

            await uow.member.add_one(account_id=account_obj.id, company_id=company_obj.id, is_admin=True)

            return SignUpCompleteResponseSchema(
                user_id=user_obj.id,
                email=account_obj.email,
                first_name=user_obj.first_name,
                last_name=user_obj.last_name,
                company_name=company_obj.name
            )

    @classmethod
    async def sign_up_employee(
        cls,
        uow: UnitOfWork,
        email: str,
        invite_token: str,
    ):
        async with uow:
            invite_obj: InviteModel = await uow.invite.get_by_query_one_or_none(
                email=email,
                token=invite_token,
                invite_type=InviteTypes.EMPLOYMENT,
            )
            if invite_obj is None:
                raise exceptions.page_not_found()

            if invite_obj.is_confirmed:
                raise exceptions.invite_token_already_confirmed()

            invite_obj.is_confirmed = True

            return SignUpResponseSchema(email=invite_obj.email)

    @classmethod
    async def register_employee(
        cls,
        uow: UnitOfWork,
        email: str,
        password: str
    ):
        async with uow:
            account_obj: AccountModel = await uow.account.get_by_query_one_or_none(email=email)
            if not account_obj or account_obj.is_active:
                raise exceptions.account_already_registered()

            invite_obj: InviteModel = await cls._get_confirmed_invite_obj_or_raise(
                uow=uow, email=email, invite_type=InviteTypes.EMPLOYMENT
            )
            if not invite_obj.is_confirmed:
                raise exceptions.account_is_not_confirmed()

            account_obj.is_active = True

            await uow.secret.change_password(
                account_id=account_obj.id,
                new_password=utils.hash_password(password)
            )
            return SignUpCompleteEmployeeResponseSchema(
                account_id=account_obj.id,
                email=email
            )

    @staticmethod
    async def _create_invite_token(uow: UnitOfWork, email: str, invite_type: str):
        token: str = str(randint(100000, 999999))

        invite_obj: InviteModel = await uow.invite.get_by_query_one_or_none(email=email)
        if invite_obj is None:
            invite_obj = await uow.invite.add_one_and_get_obj(
                email=email,
                token=token,
                invite_type=invite_type
            )
        else:
            invite_obj.token = token

        return invite_obj

    @staticmethod
    async def _confirm_invite_token(uow: UnitOfWork, email: str, invite_token: str) -> None:
        invite_obj: InviteModel = await uow.invite.get_by_query_one_or_none(
            email=email,
            token=invite_token
        )

        if invite_obj is None:
            raise exceptions.incorrect_account_or_invite_token()

        if invite_obj.is_confirmed:
            raise exceptions.invite_token_already_confirmed()

        invite_obj.is_confirmed = True

    @staticmethod
    async def _is_account_exists(uow: UnitOfWork, email: str) -> AccountModel:
        return await uow.account.get_by_query_one_or_none(email=email) is not None

    @staticmethod
    async def _get_confirmed_invite_obj_or_raise(
        uow: UnitOfWork,
        email: str,
        invite_type: str
    ) -> InviteModel:
        invite_info: dict = {
            'email': email,
            'is_confirmed': True,
            'invite_type': invite_type
        }
        _invite_obj: InviteModel = await uow.invite.get_by_query_one_or_none(**invite_info)

        if _invite_obj is None or not _invite_obj.is_confirmed:
            raise exceptions.account_is_not_confirmed()

        return _invite_obj

    @staticmethod
    async def _check_if_account_exists_or_raise(uow: UnitOfWork, email: str) -> AccountModel:
        is_account_exists: bool = await uow.account.get_by_query_one_or_none(email=email) is not None

        if is_account_exists:
            raise exceptions.account_already_registered()

    @staticmethod
    async def _add_secret_obj(
        uow: UnitOfWork,
        user_obj: UserModel,
        account_obj: AccountModel,
        password: str,
    ) -> None:
        secret: dict = {
            'user_id': user_obj.id,
            'account_id': account_obj.id,
            'password_hash': utils.hash_password(password)
        }
        await uow.secret.add_one(**secret)
