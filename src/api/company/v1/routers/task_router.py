from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.core.schemas import BaseResponseModel
from src.core.utils import UnitOfWork

from src.api.auth.v1.utils.dependencies import is_admin

from src.api.company.v1.services import TaskService
from src.api.company.v1.schemas import (
    AddTaskRequestSchema,
    AddTaskResponseSchema,
    UpdateTaskRequestSchema,
    UpdateTaskResponseSchema,
)


router: APIRouter = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.post(
    '/',
    response_model=AddTaskResponseSchema
)
async def add_task(
    data: AddTaskRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    account_id: str = payload['account_id']
    company_id: str = payload['company_id']
    response: AddTaskResponseSchema = await TaskService.add_new_task(
        uow=uow, author_id=account_id, company_id=company_id, data=data
    )
    return response


@router.patch(
    '/',
    response_model=UpdateTaskResponseSchema
)
async def update_task(
    data: UpdateTaskRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    account_id: str = payload['account_id']
    response: UpdateTaskResponseSchema = await TaskService.update_task(
        uow=uow, author_id=account_id, company_id=company_id, data=data
    )
    return response


@router.delete(
    '/',
    response_model=BaseResponseModel
)
async def delete_task(
    task_id: UUID4,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    response = await TaskService.delete_task(
        uow=uow, company_id=company_id, task_id=task_id
    )
    return response
