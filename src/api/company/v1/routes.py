from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from src.core.utils import UnitOfWork

from src.api.company.v1.services import MemberService, TaskService, PositionService

from src.api.company.v1.schemas import (
    AddMemberRequestSchema,
    AddMemberResponseSchema,

    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersEmailByAdminResponseSchema,

    UpdateUsersNameByAdminRequestSchema,
    UpdateUsersNameByAdminResponseSchema,
    
    AddPositionRequestSchema,
    AddPositionResponseSchema, 
    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,
    PositionDeleteResponseSchema,
)


router: APIRouter = APIRouter(
    prefix='/v1/company',
    tags=['v1', 'company']
)


@router.post(
    '/member',
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
        company_id=payload['company_id'],
        **member.model_dump()
    )
    return response


@router.patch(
    '/member/email',
    tags=['protected', 'for_admins'],
    response_model=UpdateUsersEmailByAdminResponseSchema
)
async def update_users_email(
    request: Request,
    data: UpdateUsersEmailByAdminRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение email работника админом."""
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: UpdateUsersEmailByAdminResponseSchema = await MemberService.update_users_email_by_admin(
        uow=uow,
        account_id=data.account_id,
        new_email=data.new_email,
        company_id=company_id
    )
    return response


@router.patch(
    '/member/name',
    tags=['protected', 'for_admins'],
    response_model=UpdateUsersNameByAdminResponseSchema
)
async def update_users_name(
    request: Request,
    data: UpdateUsersNameByAdminRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение имени работника админом."""
    payload: dict = request.state.payload
    company_id: str = payload['company_id']
    response: UpdateUsersNameByAdminResponseSchema = await MemberService.update_users_name(
        uow=uow,
        company_id=company_id,
        account_id=data.account_id,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return response


@router.post(
    '/position',
    tags=['protected', 'for_admins'],
    response_model=AddPositionResponseSchema
)
async def create_position(
    request: Request,
    data: AddPositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Создание новой позиции."""
    payload: str = request.state.payload
    company_id: str = payload['company_id']
    response: AddPositionResponseSchema = await PositionService.add_new_position(
        uow=uow,
        title=data.title,
        company_id=company_id,
        description=data.description,
    )
    return response


@router.patch(
    '/position',
    tags=['protected', 'for_admins'],
    response_model=UpdatePositionResponseSchema
)
async def update_position(
    request: Request,
    data: UpdatePositionRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Изменение существующей позиции."""
    payload: str = request.state.payload
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
    '/position',
    tags=['protected', 'for_admins'],
    response_model=PositionDeleteResponseSchema
)
async def update_position(
    request: Request,
    # data: PositionDeleteRequestSchema,
    position_id: UUID4,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: str = request.state.payload
    company_id: str = payload['company_id']
    response: PositionDeleteRequestSchema = await PositionService.delete_position(
        uow=uow, position_id=position_id, company_id=company_id
    )
    return response

# @router.delete(
#     '/struct',
#     tags=['protected', 'for_admins'],
# )
# async def delete_struct(
#     request: Request,
#     data: DeleteStructRequestSchema,
#     uow: UnitOfWork = Depends(UnitOfWork),
# ):
#     """Удаления подразделения и всех его подразделений."""
#     payload: str = request.state.payload
#     company_id: str = payload['company_id']
#     await PositionService.delete_struct(uow, struct_id=data.struct_id, company_id=company_id)


# @router.patch(
#     '/struct',
#     tags=['protected', 'for_admins']
# )
# async def update_struct(
#     request: Request,
#     data: UpdateStructRequestSchema,
#     uow: UnitOfWork = Depends(UnitOfWork)
# ):
#     """Изменение подразделения."""
#     payload: str = request.state.payload
#     company_id: str = payload['company_id']
#     response = await PositionService.update_struct(
#         uow=uow,
#         id=data.struct_id,
#         company_id=company_id,
#         new_name=data.new_name
#     )
#     return response


# @router.post(
#     '/task',
#     tags=['protected', 'for_admins'],
# )
# async def add_task(
#     request: Request,
#     data: AddTaskRequestSchema,
#     uow: UnitOfWork = Depends(UnitOfWork),
# ):
#     payload: str = request.state.payload
#     account_id: str = payload['account_id']
#     response = await TaskService.add_new_task(uow=uow, author_id=account_id, **data.model_dump(exclude_none=True))
#     return response
