from abc import ABC, abstractmethod

from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    
    @abstractmethod
    async def get_by_query_one_or_none(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def update_one_or_create_new(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_query_one_or_none(self, *args, **kwargs) -> type(model) | None:
        query = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()
    
    async def update_one_or_create_new(self, filters: dict, values: dict) -> type(model):
        query = select(self.model).filter_by(**filters)
        _obj: Result | None = await self.session.execute(query)
        if _obj.scalar_one_or_none() is None:
            stmt = insert(self.model).values(**values).returning(self.model)
        else:
            stmt = update(self.model).filter_by(**filters).values(**values).returning(self.model)
        _obj: Result | None = await self.session.execute(stmt)
        return _obj.scalar_one_or_none()
