from src.core import exceptions
from src.core.utils import BaseService, UnitOfWork
from src.celery_app.tasks import send_invite_link

from src.api.auth.v1.services import RegisterService
from src.api.auth.models import UserModel, AccountModel, InviteTypes, InviteModel
from src.api.company.schemas import (
    AddMemberResponseSchema,
    AddMemberRequestSchema,
    UpdateUsersEmailByAdminResponseSchema
)


class MemberService(BaseService):

    @classmethod
    async def add_new_member(
        cls,
        uow: UnitOfWork,
        email: str, first_name: str, last_name: str, company_id: int
    ):
        async with uow:
            await RegisterService._check_if_account_exists_or_raise(uow=uow, email=email)

            user_obj: UserModel = await uow.user.add_one_and_get_obj(
                first_name=first_name,
                last_name=last_name,
            )

            account_obj: AccountModel = await uow.account.add_one_and_get_obj(
                email=email,
                is_active=False
            )

            await RegisterService._add_secret_obj(
                uow=uow,
                user_obj=user_obj,
                account_obj=account_obj,
                password='password'
            )

            await uow.member.add_one(
                account_id=account_obj.id,
                company_id=company_id,
                is_admin=False
            )

            invite_obj: InviteModel = await RegisterService._create_invite_token(
                uow=uow,
                email=email,
                invite_type=InviteTypes.EMPLOYMENT
            )

            cls._send_invite_link(email=email, invite_token=invite_obj.token)

            return AddMemberResponseSchema(
                user=AddMemberRequestSchema(
                    email=email, first_name=first_name, last_name=last_name
                )
            )

    @classmethod
    async def update_users_email_by_admin(
        cls,
        uow: UnitOfWork,
        email: str, new_email: str, company_id: str
    ):
        async with uow:
            account_obj: AccountModel = await uow.member.get_account_by_company_id_and_email_or_none(
                company_id=company_id,
                email=email,
            )

            if account_obj is None:
                raise exceptions.incorrect_email(email=email)
            
            if await uow.account.get_by_query_one_or_none(email=new_email) is not None:
                raise exceptions.account_already_registered(new_email)
            
            account_obj.email = new_email
            
            return UpdateUsersEmailByAdminResponseSchema(new_email=new_email)

    @staticmethod
    def _send_invite_link(email: str, invite_token: str) -> None:
        invite_link: str = f'http://127.0.0.1:8000/api/v1/auth/sign-up?{email=}&{invite_token=}'
        send_invite_link.delay(to_email=email, invite_link=invite_link)
