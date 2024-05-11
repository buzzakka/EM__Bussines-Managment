from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from src.core.utils import UnitOfWork

from src.api.company.v1.services import PositionService

from src.api.company.v1.schemas import (
    AddPositionRequestSchema,
    AddPositionResponseSchema,
    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,
    DeletePositionResponseSchema,
)


router: APIRouter = APIRouter(
    prefix='/position',
    tags=['position']
)


@router.post(
    '/',
    tags=['protected', 'for_admins'],
    response_model=AddPositionResponseSchema
)
async def create_position(
    request: Request,
    data: AddPositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Создание новой позиции."""
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: AddPositionResponseSchema = await PositionService.add_new_position(
        uow=uow,
        title=data.title,
        company_id=company_id,
        description=data.description,
    )
    return response


@router.patch(
    '/',
    tags=['protected', 'for_admins'],
    response_model=UpdatePositionResponseSchema
)
async def update_position(
    request: Request,
    data: UpdatePositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение существующей позиции."""
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: AddPositionResponseSchema = await PositionService.update_position(
        uow=uow,
        position_id=data.position_id,
        company_id=company_id,
        new_title=data.new_position.title,
        new_description=data.new_position.description,
    )
    return response


@router.delete(
    '/',
    tags=['protected', 'for_admins'],
    response_model=DeletePositionResponseSchema
)
async def update_position(
    request: Request,
    position_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: DeletePositionResponseSchema = await PositionService.delete_position(
        uow=uow, position_id=position_id, company_id=company_id
    )
    return response
