from fastapi import APIRouter, Depends, Request

from src.core.utils import UnitOfWork

from src.api.company.v1.services import MemberService
from src.api.company.schemas import AddMemberRequestSchema, AddMemberResponseSchema


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
