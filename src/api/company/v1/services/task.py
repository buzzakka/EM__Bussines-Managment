from datetime import datetime

from src.core import exceptions
from src.core.utils import BaseService, UnitOfWork

from src.api.auth.models import AccountModel


class TaskService(BaseService):
    repository = 'task'

    @classmethod
    async def add_new_task(
        cls,
        uow: UnitOfWork,
        **kwargs
    ):
        async with uow:
            if 'responsible_id' in kwargs:
                responsible: AccountModel = await uow.account.get_by_query_one_or_none(id=kwargs['responsible_id'])
                if responsible is None:
                    raise exceptions.incorrect_param('responsible_id')

            await uow.task.add_task(**kwargs)

            return
