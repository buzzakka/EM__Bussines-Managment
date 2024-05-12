from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.core.utils import UnitOfWork

from src.api.auth.v1.utils.dependencies import is_admin

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
    response_model=AddStructResponseSchema
)
async def add_struct(
    data: AddStructRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    response: AddStructResponseSchema = await PositionService.add_struct(
        uow=uow,
        company_id=company_id,
        data=data
    )
    return response


@router.patch(
    '/',
    response_model=UpdateStructResponseSchema
)
async def update_struct(
    data: UpdateStructRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """Изменение подразделения."""
    company_id: str = payload['company_id']
    response: UpdateStructResponseSchema = await PositionService.update_struct(
        uow=uow,
        data=data,
        company_id=company_id,
    )
    return response


@router.delete(
    '/',
    response_model=DeleteStructResponseSchema
)
async def delete_struct(
    struct_id: UUID4,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Удаление подразделения и всех его подразделений."""
    company_id: str = payload['company_id']
    response: DeleteStructResponseSchema = await PositionService.delete_struct(
        uow=uow, struct_id=struct_id, company_id=company_id
    )
    return response


@router.post(
    '/position/',
    response_model=UpdateStructPositionResponseSchema
)
async def add_position_to_struct(
    data: AddStructPositionRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    response: UpdateStructPositionResponseSchema = await PositionService.add_position_to_struct(
        uow=uow, data=data, company_id=company_id
    )
    return response


@router.patch(
    '/position/',
    response_model=UpdateStructPositionResponseSchema
)
async def add_position_to_struct(
    data: UpdateStructPositionRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    response: AddStructPositionResponseSchema = await PositionService.update_struct_position(
        uow=uow, data=data, company_id=company_id
    )
    return response


@router.delete(
    '/position/',
    response_model=DeleteStructPositionResponseSchema
)
async def delete_struct_position(
    struct_position_id: UUID4,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    response: DeleteStructPositionResponseSchema = await PositionService.delete_struct_position(
        uow=uow, struct_position_id=struct_position_id, company_id=company_id
    )
    return response
