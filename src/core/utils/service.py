from typing import Any
from sqlalchemy import Result, Sequence
from src.core.models.base import Base
from src.core.utils.unit_of_work import UnitOfWork


class BaseService:

    repository: str

    @classmethod
    async def add_one(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> None:
        async with uow:
            await uow.__dict__[cls.repository].add_one(**kwargs)

    @classmethod
    async def add_one_and_get_obj(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Base | None:
        async with uow:
            _obj: Result = await uow.__dict__[cls.repository].add_one_and_get_obj(**kwargs)
            return _obj

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
    async def get_by_query_all(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Sequence[Any]:
        async with uow:
            _result = await uow.__dict__[cls.base_repository].get_by_query_all(**kwargs)
            return _result

    @classmethod
    async def update_one_by_id(
            cls,
            uow: UnitOfWork,
            _id: int,
            values: dict
    ) -> Base | None:
        async with uow:
            _obj = await uow.__dict__[cls.repository].update_one_by_id(_id=_id, values=values)
            return _obj

    @classmethod
    async def update_one_by_filters(
        cls,
        uow: UnitOfWork,
        filters: dict,
        values: dict
    ) -> Base | None:
        async with uow:
            _obj = await uow.__dict__[cls.repository].update_one_by_filters(filters=filters, values=values)
            return _obj

    @classmethod
    async def delete_by_query(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> None:
        async with uow:
            await uow.__dict__[cls.repository].delete_by_query(**kwargs)
