from datetime import datetime
from sqlalchemy import UUID, Result, insert, select
from sqlalchemy.orm import selectinload

from src.core.utils import SqlAlchemyRepository

from src.api.auth.models import AccountModel
from src.api.company.models import TaskModel, MemberModel


class TaskRepository(SqlAlchemyRepository):
    model = TaskModel

    async def add_task(
        self,
        observers: list[str] | None = None,
        performers: list[str] | None = None,
        **kwargs
    ):
        query = (
            insert(self.model)
            .returning(self.model)
            .values(**kwargs)
            .options(selectinload(TaskModel.performers))
            .options(selectinload(TaskModel.observers))
        )

        obj: Result = await self.session.execute(query)

        await self.session.flush()

        task: TaskModel = obj.scalars().first()

        if observers:
            query = select(AccountModel).filter(AccountModel.id.in_(observers))
            account_objs: Result = await self.session.execute(query)
            for account in account_objs.scalars().all():
                task.observers.append(account)

        if performers:
            query = select(AccountModel).filter(
                AccountModel.id.in_(performers))
            account_objs: Result = await self.session.execute(query)
            for account in account_objs.scalars().all():
                task.performers.append(account)
        
        return task 

    async def get_companys_members_by_ids(
        self,
        ids: list[UUID],
        company_id: UUID
    ):
        query = (
            select(MemberModel)
            .where(MemberModel.account_id.in_(ids), MemberModel.company_id == company_id)
        )
        result: Result = await self.session.execute(query)
        return result.scalars().all()
