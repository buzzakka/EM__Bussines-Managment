from fastapi import APIRouter, Depends, Request

from src.core.utils import UnitOfWork
from src.core.schemas import BaseResponseModel
from src.api.auth.v1.services import AuthService
from src.api.auth.schemas import (
    UserLoginResponseSchema,
    UserLoginRequestSchema,
    TokenSchema
)

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
    tags=['protected'],
    response_model=BaseResponseModel
)
async def logout(
    request: Request,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    account_id: int = request.state.payload['account_id']
    await AuthService.logout(uow=uow, account_id=account_id)
    return BaseResponseModel()
