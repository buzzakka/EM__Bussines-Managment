from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import EmailStr

from src.core.utils import UnitOfWork
from src.api.auth import exceptions
from src.api.auth.v1 import utils
from src.api.auth.v1.services import (
    SecretService,
    RegistrationService,
    AccountService,
    InviteService
)
from src.api.auth.v1.models import AccountModel
from src.api.auth.v1.schemas import (
    TokenSchema,
    SignUpCompleteRequestSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
    UserLoginSchema,
    SignUpCompleteResponseSchema,
)

http_bearer = HTTPBearer()


router: APIRouter = APIRouter(
    prefix='/v1/auth',
    tags=['v1', 'auth']
)


@router.get(
    path='/check_account/{account}'
)
async def check_account(
    account: EmailStr,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    is_account_exists: AccountModel = await AccountService.is_account_exists(uow=uow, email=account)

    if is_account_exists:
        raise exceptions.account_already_registered()

    invite = await InviteService.create_invite_token(uow=uow, email=account)

    return invite


@router.post(
    path='/sign-up',
    response_model=SignUpResponseSchema
)
async def sign_up(
    user_data: SignUpRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    email: str = user_data.account
    token: str = user_data.invite_token

    is_account_exists: bool = await AccountService.is_account_exists(uow, email)

    if is_account_exists:
        raise exceptions.account_already_registered()

    await InviteService.check_invite_token(uow, email, token)

    return SignUpResponseSchema(account=user_data.account)


@router.post(
    path='/sign-up-complete',
    response_model=SignUpCompleteResponseSchema
)
async def sign_up_complete(
    user_data: SignUpCompleteRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    response_data: dict = await RegistrationService.register_user(
        uow=uow,
        user_data=user_data.model_dump()
    )
    return response_data


@router.post('/login', response_model=TokenSchema)
async def auth_user(
    user: UserLoginSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    hashed_password: bytes = await SecretService.get_password_by_email(uow, user.email)

    is_valid_password: bool = utils.validate_password(
        user.password,
        hashed_password
    )

    if not is_valid_password:
        raise exceptions.incorrect_email_or_password()

    payload: dict = {
        'sub': user.email,
        'email': user.email
    }
    token: str = utils.encode_jwt(payload=payload)
    return TokenSchema(access_token=token, token_type='Bearer')
