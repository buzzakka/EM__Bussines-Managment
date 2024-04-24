from src.api.auth.v1.services.account import AccountService
from src.api.auth.v1.exceptions import RegistrationError
from src.api.auth.v1.utils import hash_password

from src.api.auth.v1.models.user import UserModel
from src.api.auth.v1.models.account import AccountModel
from src.api.auth.v1.models.invite import InviteModel

from src.core.utils.unit_of_work import UnitOfWork
from src.core.utils.service import BaseService


class AuthService(BaseService):

    @classmethod
    async def register_user(
        cls,
        uow: UnitOfWork,
        user_data: dict
    ):
        async with uow:
            invite_info: dict = cls._generate_invite_info(user_data)
            _invite: InviteModel = await uow.invite.get_by_query_one_or_none(**invite_info)

            if _invite is None or not _invite.is_confirmed:
                raise RegistrationError(
                    'Адрес аэлектронной почты не подтвержден.'
                )

            is_account_exists: bool = await AccountService.is_account_exists(uow=uow, email=user_data.get('account'))

            if is_account_exists:
                raise RegistrationError(
                    'Адрес электронной почты уже зарегестрирован.'
                )

            user_info: dict = cls._generate_user_info(user_data)
            user_obj: UserModel = await uow.user.add_one_and_get_obj(**user_info)

            account_obj: AccountModel = await uow.account.add_one_and_get_obj(email=user_data.get('account'))

            secret_info: dict = cls._generate_secret_info(user_obj, account_obj, user_data.get('password'))
            await uow.secret.add_one(**secret_info)
            
            await uow.company.add_one(name=user_data.get('company_name'))

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
            'password_hash': hash_password(password)
        }
