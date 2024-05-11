from datetime import datetime
from pydantic import UUID4
from sqlalchemy import UUID, Result, delete, insert, select, update
from sqlalchemy.orm import selectinload

from src.core.utils import SqlAlchemyRepository

from src.api.auth.models import AccountModel
from src.api.company.models import TaskModel, MemberModel, TaskObserversModel, TaskPerformersModel


class TaskRepository(SqlAlchemyRepository):
    model = TaskModel

    async def add_task(
        self,
        observers: list[UUID4] | None = None,
        performers: list[UUID4] | None = None,
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

    async def update_task(
        self,
        task_id: UUID4,
        observers: list[UUID4] | None = None,
        performers: list[UUID4] | None = None,
        **kwargs
    ):
        update_query = (
            update(self.model)
            .where(self.model.id == task_id)
            .values(**kwargs)
            .returning(self.model)
        )
        obj: Result = await self.session.execute(update_query)
        task: TaskModel = obj.scalars().first()

        if observers is not None:
            # Удаляем существующих наблюдателей
            stmt = (
                delete(TaskObserversModel)
                .where(TaskObserversModel.task_id == task_id)
            )
            await self.session.execute(stmt)

            # Добавляем новых наблюдателей
            query = select(AccountModel).filter(AccountModel.id.in_(observers))
            account_objs: Result = await self.session.execute(query)
            for account in account_objs.scalars().all():
                task.observers.append(account)

        if performers is not None:
            # Удаляем существующих наблюдателей
            stmt = delete(TaskPerformersModel).where(
                TaskPerformersModel.task_id == task_id)
            await self.session.execute(stmt)

            # Добавляем новых наблюдателей
            query = select(AccountModel).filter(
                AccountModel.id.in_(performers))
            account_objs: Result = await self.session.execute(query)
            for account in account_objs.scalars().all():
                task.performers.append(account)

        return task

    async def get_companys_members_by_ids(
        self,
        ids: list[UUID4],
        company_id: UUID4
    ):
        query = (
            select(MemberModel)
            .where(MemberModel.account_id.in_(ids), MemberModel.company_id == company_id)
        )
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def get_task(
        self, company_id: UUID4, task_id: UUID4
    ):
        query = (
            select(self.model)
            .join(AccountModel, AccountModel.id == self.model.author_id)
            .join(MemberModel, AccountModel.id == MemberModel.account_id)
            .where(MemberModel.company_id == company_id, self.model.id == task_id)
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()
