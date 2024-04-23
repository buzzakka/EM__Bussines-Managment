from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.api.auth.v1.models.user import UserModel
from src.api.auth.v1.services.user import UserService
from src.core.utils.unit_of_work import UnitOfWork

router: APIRouter = APIRouter(
    prefix='/v1',
    tags=['v1']
)


@router.get(
    path='/check_account/{account}'
)
async def check_account(
    account: EmailStr,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    user: UserModel = await UserService.get_by_query_one_or_none(uow=uow, email=account)
    return user
