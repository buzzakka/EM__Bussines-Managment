from random import randint

from src.core.utils.unit_of_work import UnitOfWork
from src.api.auth.v1.models.invite import InviteModel
from src.core.utils.service import BaseService


class InviteService(BaseService):
    repository: str = 'invite'
    
    @classmethod
    async def create_invite_token(cls, uow: UnitOfWork, email: str):
        _obj: InviteModel = await cls.get_by_query_one_or_none(uow=uow, email=email)
        
        if _obj is not None and _obj.is_confirmed:
            pass
        
        filters: dict = {'email': email}
        values: dict = {'email': email, 'token': str(randint(100000, 999999))}
        
        _obj: InviteModel = await cls.update_one_or_create_new(uow=uow, filters=filters, values=values)
        return _obj
