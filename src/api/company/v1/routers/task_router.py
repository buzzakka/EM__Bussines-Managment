from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from src.core.schemas import BaseResponseModel
from src.core.utils import UnitOfWork

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
    tags=['protected', 'for_admins'],
    response_model=AddTaskResponseSchema
)
async def add_task(
    request: Request,
    data: AddTaskRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    account_id: str = payload['account_id']
    company_id: str = payload['company_id']
    response: AddTaskResponseSchema = await TaskService.add_new_task(
        uow=uow, author_id=account_id, company_id=company_id, data=data
    )
    return response


@router.patch(
    '/',
    tags=['protected', 'for_admins'],
    response_model=UpdateTaskResponseSchema
)
async def update_task(
    request: Request,
    data: UpdateTaskRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    account_id: str = payload['account_id']
    response: UpdateTaskResponseSchema = await TaskService.update_task(
        uow=uow, author_id=account_id, company_id=company_id, data=data
    )
    return response


@router.delete(
    '/',
    tags=['protected', 'for_admins'],
    response_model=BaseResponseModel
)
async def delete_task(
    request: Request,
    task_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response = await TaskService.delete_task(
        uow=uow, company_id=company_id, task_id=task_id
    )
    return response
