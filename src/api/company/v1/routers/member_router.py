from fastapi import APIRouter, Depends, Request

from src.core.utils import UnitOfWork

from src.api.auth.v1.utils.dependencies import is_admin
from src.api.company.v1.services import MemberService
from src.api.company.v1.schemas import (
    AddMemberRequestSchema,
    AddMemberResponseSchema,

    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersEmailByAdminResponseSchema,

    UpdateUsersNameByAdminRequestSchema,
    UpdateUsersNameByAdminResponseSchema,
)


router: APIRouter = APIRouter(
    prefix='/member',
    tags=['member']
)


@router.post(
    '/',
    response_model=AddMemberResponseSchema
)
async def add_new_member(
    member: AddMemberRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Добавление админом нового работника."""
    response: AddMemberResponseSchema = await MemberService.add_new_member(
        uow=uow,
        company_id=payload['company_id'],
        **member.model_dump()
    )
    return response


@router.patch(
    '/email',
    response_model=UpdateUsersEmailByAdminResponseSchema
)
async def update_users_email(
    data: UpdateUsersEmailByAdminRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение email работника админом."""
    company_id: str = payload['company_id']
    response: UpdateUsersEmailByAdminResponseSchema = await MemberService.update_users_email_by_admin(
        uow=uow,
        account_id=data.account_id,
        new_email=data.new_email,
        company_id=company_id
    )
    return response


@router.patch(
    '/name',
    response_model=UpdateUsersNameByAdminResponseSchema
)
async def update_users_name(
    data: UpdateUsersNameByAdminRequestSchema,
    payload: dict = Depends(is_admin),
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение имени работника админом."""
    company_id: str = payload['company_id']
    response: UpdateUsersNameByAdminResponseSchema = await MemberService.update_users_name(
        uow=uow,
        company_id=company_id,
        account_id=data.account_id,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return response
