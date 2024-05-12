from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.utils import BaseService, UnitOfWork, bad_responses
from src.core.schemas import BaseResponseModel

from src.api.company.models import TaskModel
from src.api.company.v1.schemas import (
    AddTaskRequestSchema,
    AddTaskResponseSchema,
    UpdateTaskRequestSchema,
    UpdateTaskResponseSchema,
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
                payload=task.to_pydantic_schema()
            )

    @classmethod
    async def update_task(
        cls,
        uow: UnitOfWork,
        company_id: UUID4, author_id: UUID4,
        data: UpdateTaskRequestSchema
    ) -> UpdateTaskResponseSchema:
        async with uow:
            await cls._check_ids(
                uow,
                company_id, author_id,
                data.responsible_id, data.observers, data.performers
            )

            await cls._check_task_id(uow, data.task_id, company_id)

            task: TaskModel = await uow.task.update_task(**data.model_dump(exclude_unset=True))

            return UpdateTaskResponseSchema(
                payload=task.to_pydantic_schema()
            )

    @classmethod
    async def delete_task(
        cls,
        uow: UnitOfWork,
        company_id: UUID4, task_id: UUID4
    ):
        async with uow:
            task: TaskModel = await cls._check_task_id(uow, task_id, company_id)

            await uow.task.delete_by_query(id=task_id)

            return UpdateTaskResponseSchema(
                payload=task.to_pydantic_schema()
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Один из введенных id аккаунта некорректен.'
            )

    @classmethod
    async def _check_task_id(
        cls,
        uow: UnitOfWork,
        task_id: UUID4, company_id: UUID4
    ) -> TaskModel:
        task_obj: TaskModel | None = await uow.task.get_task(company_id=company_id, task_id=task_id)
        if task_obj is None:
            raise bad_responses.bad_param('task_id')
        return task_obj
