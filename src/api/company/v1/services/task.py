from fastapi import status
from pydantic import UUID4

from src.core.utils import BaseService, UnitOfWork
from src.core.schemas import BaseResponseModel

from src.api.company.models import TaskModel
from src.api.company.v1.schemas import (
    AddTaskRequestSchema,
    AddTaskResponseSchema,
    AddTaskPayloadSchema
)


class TaskService(BaseService):
    repository = 'task'

    @classmethod
    async def add_new_task(
        cls,
        uow: UnitOfWork,
        company_id: UUID4,
        author_id: UUID4,
        data: AddTaskRequestSchema
    ) -> AddTaskResponseSchema:
        async with uow:
            try:
                await cls._check_ids(
                    uow,
                    company_id,
                    author_id,
                    data.responsible_id,
                    data.observers,
                    data.performers
                )
            except ValueError:
                return BaseResponseModel(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error=False,
                    message='Один из введенных id неверный.'
                )

            task: TaskModel = await uow.task.add_task(author_id=author_id, **data.model_dump())

            return AddTaskResponseSchema(
                payload=AddTaskPayloadSchema(
                    task_id=task.id,
                    **data.model_dump(),
                )
            )

    @classmethod
    async def _check_ids(
        cls,
        uow: UnitOfWork,
        company_id: UUID4,
        author_id: UUID4, responsible_id: UUID4 | None,
        observers: list[UUID4] | None, performers: list[UUID4] | None
    ):
        user_ids: set[UUID4] = {author_id, }
        if responsible_id:
            user_ids.add(str(responsible_id))
        if observers is not None:
            user_ids.update([str(id) for id in observers])
        if performers is not None:
            user_ids.update([str(id) for id in performers])

        members = await uow.task.get_companys_members_by_ids(ids=user_ids, company_id=company_id)
        if len(user_ids) != len(members):
            raise ValueError
