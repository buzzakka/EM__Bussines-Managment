from fastapi import APIRouter, Depends, Request
from pydantic import Field, EmailStr

from src.core.utils import UnitOfWork

from src.api.company.v1.services import MemberService, PositionService
from src.api.company.schemas import (
    AddMemberRequestSchema,
    AddMemberResponseSchema,
    UpdateUsersEmailByAdminResponseSchema,
    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersNameByAdminRequeestSchema,
    AddPositionRequestSchema,
    AddPositionResponseSchema,
    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,
)


router: APIRouter = APIRouter(
    prefix='/v1/company',
    tags=['v1', 'company']
)


@router.post(
    '/add-member',
    tags=['protected', 'for_admins'],
    response_model=AddMemberResponseSchema
)
async def add_new_member(
    request: Request,
    member: AddMemberRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Добавление админом нового работника."""
    payload: dict = request.state.payload
    response: AddMemberResponseSchema = await MemberService.add_new_member(
        uow=uow,
        email=member.email,
        first_name=member.first_name,
        last_name=member.last_name,
        company_id=payload['company_id']
    )
    return response


@router.patch('/update-users-email', tags=['protected', 'for_admins'])
async def update_users_email(
    request: Request,
    data: UpdateUsersEmailByAdminRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: int = payload['company_id']
    response: UpdateUsersEmailByAdminResponseSchema = await MemberService.update_users_email_by_admin(
        uow=uow,
        account_id=data.account_id,
        new_email=data.new_email,
        company_id=company_id
    )
    return response


@router.patch('/update-users-name', tags=['protected', 'for_admins'])
async def update_users_email(
    request: Request,
    data: UpdateUsersNameByAdminRequeestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: int = payload['company_id']
    response: UpdateUsersEmailByAdminResponseSchema = await MemberService.update_users_name(
        uow=uow,
        company_id=company_id,
        account_id=data.account_id,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return response


@router.post(
    '/create-position',
    tags=['protected', 'for_admins'],
    response_model=AddPositionResponseSchema
)
async def create_position(
    request: Request,
    data: AddPositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: str = request.state.payload
    company_id: int = payload['company_id']
    response: AddPositionResponseSchema = await PositionService.add_new_position(
        uow=uow,
        title=data.title,
        company_id=company_id,
        description=data.description,
    )
    return response


@router.patch(
    '/update-position',
    tags=['protected', 'for_admins'],
    response_model=UpdatePositionResponseSchema
)
async def update_position(
    request: Request,
    data: UpdatePositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: str = request.state.payload
    company_id: int = payload['company_id']
    response: AddPositionResponseSchema = await PositionService.update_position(
        uow=uow,
        position_id=data.position_id,
        company_id=company_id,
        new_title=data.new_position.title,
        new_description=data.new_position.description,
    )
    return response
