from fastapi import APIRouter, Depends, Request
from pydantic import EmailStr

from src.core.utils import UnitOfWork
from src.core.schemas import BaseResponseModel
from src.api.auth.v1.services import RegisterService, AuthService
from src.api.auth.schemas import (
    UserLoginResponseSchema,
    UserLoginRequestSchema,
    TokenSchema
)
from src.api.auth.v1.schemas import (
    CheckAccountResponseSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
    AccountRegisterRequestSchema,
    AccountRegisterResponseSchema,
    EmployeConfirmResponseSchema,
    EmployeeSignUpCompleteRequestSchema,
    EmployeeSignUpCompleteResponseSchema,
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
    data: SignUpRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """Подтверждение инвайт кода."""
    sign_up_response: SignUpResponseSchema = await RegisterService.sign_up_company(
        uow=uow,
        email=data.account,
        token=data.invite_token
    )

    return sign_up_response


@router.post(
    path='/sign-up-complete',
    response_model=AccountRegisterResponseSchema
)
async def sign_up_complete(
    user_data: AccountRegisterRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    """Регистрация компании."""
    sign_up_complete_response: dict = await RegisterService.register_company(
        uow=uow,
        **user_data.model_dump()
    )
    return sign_up_complete_response


@router.get(
    path='/sign-up-employee',
    response_model=EmployeConfirmResponseSchema
)
async def check_account_with_token(
    email: EmailStr,
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
    response_model=EmployeeSignUpCompleteResponseSchema
)
async def sign_up_complete_employmee(
    user_data: EmployeeSignUpCompleteRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    response: dict = await RegisterService.register_employee(
        uow=uow,
        **user_data.model_dump()
    )
    return response


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
