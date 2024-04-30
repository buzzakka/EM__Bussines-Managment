from random import randint

from src.core.utils import UnitOfWork, BaseService
from src.celery_app.tasks import send_invite_token

from src.api.auth import exceptions
from src.api.auth.models import InviteModel


class InviteService(BaseService):
    repository: str = 'invite'

    @classmethod
    async def create_invite_token(cls, uow: UnitOfWork, email: str):
        token: str = str(randint(100000, 999999))
        filters: dict = {'email': email}
        values: dict = {'email': email, 'token': token}

        _obj: InviteModel = await cls.update_one_or_create_new(
            uow=uow,
            filters=filters,
            values=values
        )

        send_invite_token.delay(email=email, invite_token=token)

        return _obj

    @classmethod
    async def check_invite_token(cls, uow: UnitOfWork, email: str, token: str):
        db_token: InviteModel = await cls.get_by_query_one_or_none(
            uow, email=email, token=token
        )

        if db_token is None:
            raise exceptions.incorrect_account_or_invite_token()

        if db_token.is_confirmed:
            raise exceptions.invite_token_already_confirmed()

        await cls.update_one_by_id(uow=uow, _id=db_token.id, values={'is_confirmed': True})
