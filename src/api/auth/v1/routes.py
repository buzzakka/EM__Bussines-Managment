from fastapi import APIRouter, Depends, Request
from pydantic import EmailStr

from src.core.utils import UnitOfWork

from src.api.auth.v1.services import RegisterService, AuthService
from src.api.auth.schemas import (
    TokenSchema,
    SignUpCompleteRequestSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
    UserLoginSchema,
    SignUpCompleteResponseSchema,
    CheckAccountResponseSchema,
    SignUpCompleteEmploymeeRequestSchema,
    SignUpCompleteEmployeeResponseSchema,
)

router: APIRouter = APIRouter(
    prefix='/v1/auth',
    tags=['v1', 'auth']
)


@router.get(
    path='/check_account/{account}',
    response_model=CheckAccountResponseSchema
)
async def check_account_with_email(
    account: EmailStr,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """Проверка, что почта свободна."""
    check_account_response: CheckAccountResponseSchema = await RegisterService.check_account(
        uow=uow,
        email=account
    )
    return check_account_response


@router.post(
    path='/sign-up',
    response_model=SignUpResponseSchema
)
async def sign_up(
    sign_up_data: SignUpRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """Подтверждение инвайт кода."""
    sign_up_response: SignUpResponseSchema = await RegisterService.sign_up_company(
        uow=uow,
        sign_up_data=sign_up_data
    )

    return sign_up_response


@router.post(
    path='/sign-up-complete',
    response_model=SignUpCompleteResponseSchema
)
async def sign_up_complete(
    user_data: SignUpCompleteRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Регистрация компании."""
    sign_up_complete_response: dict = await RegisterService.register_company(
        uow=uow,
        **user_data.model_dump()
    )
    return sign_up_complete_response


@router.get('/sign-up-employee')
async def check_account_with_token(
    email: str,
    invite_token: str,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    response: dict = await RegisterService.sign_up_employee(
        uow=uow,
        email=email,
        invite_token=invite_token,
    )
    return response


@router.post(
    path='/sign-up-employee',
    response_model=SignUpCompleteEmployeeResponseSchema
)
async def sign_up_complete_employmee(
    user_data: SignUpCompleteEmploymeeRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    response: dict = await RegisterService.register_employee(
        uow=uow,
        **user_data.model_dump()
    )
    return response


@router.post('/login', response_model=TokenSchema)
async def login(
    user: UserLoginSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    login_response: TokenSchema = await AuthService.login(
        uow=uow,
        user=user
    )
    return login_response


@router.post('/logout', tags=['protected'])
async def logout(
    request: Request,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    account_id: int = request.state.payload['account_id']
    await AuthService.logout(uow=uow, account_id=account_id)
    return
