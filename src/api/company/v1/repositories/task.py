from datetime import datetime
from sqlalchemy import Result, insert, select
from sqlalchemy.orm import selectinload
from src.api.auth.models import AccountModel
from src.api.company.models import TaskModel
from src.core.utils import SqlAlchemyRepository


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
            query = select(AccountModel).filter(AccountModel.id.in_(performers))
            account_objs: Result = await self.session.execute(query)
            for account in account_objs.scalars().all():
                task.performers.append(account)
                
            
        
        
        
    
    # async def add_observer(self):
    #     stmt = (
    #         select(self.model)
    #         .filter_by(id='31594db3-50af-48ef-9445-c181322cc254')
    #         .options(selectinload(TaskModel.performers))
    #     )
    #     res: Result = await self.session.execute(stmt)
        
    #     task = res
        
    #     user = await self.session.execute(
    #         select(UserModel).filter_by(id='4814245e-d630-4fc2-a4e0-0a093fd6bc5d')
    #     )
        
    #     task = task.scalar_one()
    #     user = user.scalar_one()
    #     print(task)
    #     print(user)
        
    #     task.performers.append(user)
        
