from src.core.models.base import Base
from src.core.utils.unit_of_work import UnitOfWork


class BaseService:

    repository: str
    
    @classmethod
    async def get_by_query_one_or_none(
        cls,
        uow: UnitOfWork,
        **kwargs
    ) -> Base | None:
        async with uow:
            _obj: Base = await uow.__dict__[cls.repository].get_by_query_one_or_none(**kwargs)
            return _obj
    
    @classmethod
    async def update_one_or_create_new(
        cls,
        uow: UnitOfWork,
        filters: dict,
        values: dict
    ) -> Base | None:
        async with uow:
            _obj: Base = await uow.__dict__[cls.repository].update_one_or_create_new(filters=filters, values=values)
            return _obj
