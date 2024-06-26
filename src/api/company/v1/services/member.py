from src.celery_app.tasks import send_invite_link

from src.core.utils import BaseService, UnitOfWork
from src.core.utils import bad_responses as core_bade_responses

from src.api.auth.models import UserModel, AccountModel, InviteTypes, InviteModel
from src.api.auth.utils import bad_responses as auth_bad_responses
from src.api.auth.v1.services import RegisterService

from src.api.company.models import MemberModel
from src.api.company.v1.schemas import (
    AddMemberResponseSchema,
    UpdateUsersEmailByAdminResponseSchema,
    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersNameByAdminRequestSchema,
    UpdateUsersNameByAdminResponseSchema,
)


class MemberService(BaseService):

    @classmethod
    async def add_new_member(
        cls,
        uow: UnitOfWork,
        email: str, first_name: str, last_name: str, company_id: int
    ) -> AddMemberResponseSchema:
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

            member: MemberModel = await uow.member.add_one_and_get_obj(
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
                payload=member.to_pydantic_schema()
            )

    @classmethod
    async def update_users_email_by_admin(
        cls,
        uow: UnitOfWork,
        account_id: str, new_email: str, company_id: str
    ):
        async with uow:
            account_obj: AccountModel = await uow.member.get_account_by_company_id_and_account_id_or_none(
                company_id=company_id,
                account_id=account_id,
            )

            if account_obj is None:
                raise core_bade_responses.bad_param('account_id')

            if await uow.account.get_by_query_one_or_none(email=new_email) is not None:
                raise auth_bad_responses.account_exists_response()

            account_obj.email = new_email

            return UpdateUsersEmailByAdminResponseSchema(
                payload=UpdateUsersEmailByAdminRequestSchema(
                    account_id=account_id, new_email=new_email
                )
            )

    @classmethod
    async def update_users_name(
        cls,
        uow: UnitOfWork,
        company_id: str, account_id: str, first_name: str, last_name: str
    ):
        async with uow:
            user_obj: UserModel = await uow.member.get_user_by_company_id_and_account_id_or_none(
                company_id=company_id,
                account_id=account_id,
            )
            if user_obj is None:
                raise core_bade_responses.bad_param('account_id')

            user_obj.first_name = first_name
            user_obj.last_name = last_name

            return UpdateUsersNameByAdminResponseSchema(
                payload=UpdateUsersNameByAdminRequestSchema(
                    account_id=account_id, first_name=first_name, last_name=last_name
                )
            )

    @staticmethod
    def _send_invite_link(email: str, invite_token: str) -> None:
        invite_link: str = f'http://127.0.0.1:8000/api/v1/auth/sign-up?{email=}&{invite_token=}'
        send_invite_link.delay(to_email=email, invite_link=invite_link)
