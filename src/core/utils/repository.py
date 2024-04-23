from abc import ABC, abstractmethod

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    
    @abstractmethod
    async def get_by_query_one_or_none(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_query_one_or_none(self, *args, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()
