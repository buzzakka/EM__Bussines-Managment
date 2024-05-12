from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from src.core.utils import UnitOfWork

from src.api.auth.v1.utils.dependencies import is_admin

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
    response_model=AddPositionResponseSchema
)
async def create_position(
    data: AddPositionRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Создание новой позиции."""

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
    response_model=UpdatePositionResponseSchema
)
async def update_position(
    data: UpdatePositionRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение существующей позиции."""

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
    response_model=DeletePositionResponseSchema
)
async def update_position(
    position_id: UUID4,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    company_id: str = payload['company_id']
    response: DeletePositionResponseSchema = await PositionService.delete_position(
        uow=uow, position_id=position_id, company_id=company_id
    )
    return response
