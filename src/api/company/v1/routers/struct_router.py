from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from src.core.utils import UnitOfWork

from src.api.company.v1.services import PositionService

from src.api.company.v1.schemas import (
    AddStructRequestSchema,
    AddStructResponseSchema,
    UpdateStructRequestSchema,
    UpdateStructResponseSchema,
    DeleteStructResponseSchema,

    AddStructPositionRequestSchema,
    AddStructPositionResponseSchema,
    UpdateStructPositionRequestSchema,
    UpdateStructPositionResponseSchema,
    DeleteStructPositionResponseSchema,
)


router: APIRouter = APIRouter(
    prefix='/struct',
    tags=['struct']
)


@router.post(
    '/',
    tags=['protected', 'for_admins'],
    response_model=AddStructResponseSchema
)
async def add_struct(
    request: Request,
    data: AddStructRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: AddStructResponseSchema = await PositionService.add_struct(
        uow=uow,
        company_id=company_id,
        data=data
    )
    return response


@router.patch(
    '/',
    tags=['protected', 'for_admins'],
    response_model=UpdateStructResponseSchema
)
async def update_struct(
    request: Request,
    data: UpdateStructRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """Изменение подразделения."""
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: UpdateStructResponseSchema = await PositionService.update_struct(
        uow=uow,
        data=data,
        company_id=company_id,
    )
    return response


@router.delete(
    '/',
    tags=['protected', 'for_admins'],
    response_model=DeleteStructResponseSchema
)
async def delete_struct(
    request: Request,
    struct_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Удаление подразделения и всех его подразделений."""
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: DeleteStructResponseSchema = await PositionService.delete_struct(
        uow=uow, struct_id=struct_id, company_id=company_id
    )
    return response


@router.post(
    '/position/',
    tags=['protected', 'for_admins'],
    response_model=UpdateStructPositionResponseSchema
)
async def add_position_to_struct(
    request: Request,
    data: AddStructPositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: UpdateStructPositionResponseSchema = await PositionService.add_position_to_struct(
        uow=uow, data=data, company_id=company_id
    )
    return response


@router.patch(
    '/position/',
    tags=['protected', 'for_admins'],
    response_model=UpdateStructPositionResponseSchema
)
async def add_position_to_struct(
    request: Request,
    data: UpdateStructPositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: AddStructPositionResponseSchema = await PositionService.update_struct_position(
        uow=uow, data=data, company_id=company_id
    )
    return response


@router.delete(
    '/position/',
    tags=['protected', 'for_admins'],
    response_model=DeleteStructPositionResponseSchema
)
async def delete_struct_position(
    request: Request,
    struct_position_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: DeleteStructPositionResponseSchema = await PositionService.delete_struct_position(
        uow=uow, struct_position_id=struct_position_id, company_id=company_id
    )
    return response
