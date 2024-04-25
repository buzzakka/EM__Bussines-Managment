from random import randint

from fastapi import HTTPException

from src.core.utils import UnitOfWork, BaseService
from src.api.auth import exceptions
from src.api.auth.v1.models import InviteModel


class InviteService(BaseService):
    repository: str = 'invite'

    @classmethod
    async def create_invite_token(cls, uow: UnitOfWork, email: str):
        filters: dict = {'email': email}
        values: dict = {'email': email, 'token': str(randint(100000, 999999))}

        _obj: InviteModel = await cls.update_one_or_create_new(
            uow=uow,
            filters=filters,
            values=values
        )
        return _obj

    @classmethod
    async def check_invite_token(cls, uow: UnitOfWork, email: str, token: str):
        db_token: InviteModel = await cls.get_by_query_one_or_none(
            uow, email=email, token=token
        )

        if db_token is None:
            raise exceptions.incorrect_account_or_invite_token()

        await cls.update_one_by_id(uow=uow, _id=db_token.id, values={'is_confirmed': True})
