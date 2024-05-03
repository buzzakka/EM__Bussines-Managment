from fastapi import APIRouter, Depends, Request
from pydantic import Field, EmailStr

from src.core.utils import UnitOfWork

from src.api.company.v1.services import MemberService
from src.api.company.schemas import (
    AddMemberRequestSchema,
    AddMemberResponseSchema,
    UpdateUsersEmailByAdminResponseSchema,
    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersNameByAdminRequeestSchema,
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
    payload: dict = request.state.payload
    response: AddMemberResponseSchema = await MemberService.add_new_member(
        uow=uow,
        email=member.email,
        first_name=member.first_name,
        last_name=member.last_name,
        company_id=payload['company_id']
    )
    return response


@router.post('/update-users-email', tags=['protected', 'for_admins'])
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


@router.post('/update-users-name', tags=['protected', 'for_admins'])
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
