from fastapi import APIRouter, Depends, Request

from src.core.utils import UnitOfWork
from src.core.schemas import BaseResponseModel
from src.api.auth.v1.services import AuthService
from src.api.auth.schemas import (
    UserLoginResponseSchema,
    UserLoginRequestSchema,
    TokenSchema
)

from src.api.auth.v1.utils.dependencies import is_authenticated_user

router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/login', response_model=UserLoginResponseSchema)
async def login(
    data: UserLoginRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    login_response: TokenSchema = await AuthService.login(
        uow=uow,
        email=data.email,
        password=data.password
    )
    return login_response


@router.post(
    path='/logout',
    response_model=BaseResponseModel
)
async def logout(
    uow: UnitOfWork = Depends(UnitOfWork),
    payload: dict = Depends(is_authenticated_user)
):
    account_id: int = payload['account_id']
    await AuthService.logout(uow=uow, account_id=account_id)
    return BaseResponseModel()
