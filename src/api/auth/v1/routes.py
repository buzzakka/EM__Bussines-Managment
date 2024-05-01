from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.core.utils import UnitOfWork
from src.api.auth.v1.dependencies import get_current_account
from src.api.auth.v1.services import AccountService
from src.api.auth.schemas import (
    TokenSchema,
    SignUpCompleteRequestSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
    UserLoginSchema,
    SignUpCompleteResponseSchema,
    CheckAccountResponseSchema,
    SignUpCompleteEmploymentRequestSchema
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
    check_account_response: CheckAccountResponseSchema = await AccountService.check_account(
        uow=uow,
        email=account
    )
    return check_account_response


# @router.post(
#     path='/sign-up',
#     response_model=SignUpResponseSchema
# )
# async def sign_up(
#     sign_up_data: SignUpRequestSchema,
#     uow: UnitOfWork = Depends(UnitOfWork)
# ):
#     sign_up_response: SignUpResponseSchema = await AccountService.sign_up_company(
#         uow=uow,
#         sign_up_data=sign_up_data
#     )

#     return sign_up_response


# @router.get('/sign-up/{invite_id}/{invite_token}')
# async def check_account_with_token(
#     invite_id: int,
#     invite_token: str,
#     uow: UnitOfWork = Depends(UnitOfWork)
# ):
#     await AccountService.sign_up_emloyment_user(
#         uow=uow,
#         invite_id=invite_id,
#         invite_token=invite_token,
#     )


# @router.post(
#     path='/sign-up-complete',
#     response_model=SignUpCompleteResponseSchema
# )
# async def sign_up_complete(
#     user_data: SignUpCompleteRequestSchema,
#     uow: UnitOfWork = Depends(UnitOfWork),
# ):
#     sign_up_complete_response: dict = await AccountService.register_company(
#         uow=uow,
#         **user_data.model_dump()
#     )
#     return sign_up_complete_response


# @router.post(
#     path='/sign-up-complete-employment'
# )
# async def sign_up_complete_employment(
#     user_data: SignUpCompleteEmploymentRequestSchema,
#     uow: UnitOfWork = Depends(UnitOfWork),
# ):
#     response: dict = await AccountService.register_employment_user(
#         uow=uow,
#         **user_data.model_dump()
#     )
#     return response


# @router.post('/login', response_model=TokenSchema)
# async def auth_user(
#     user: UserLoginSchema,
#     uow: UnitOfWork = Depends(UnitOfWork)
# ):
#     login_response: TokenSchema = await AccountService.login(
#         uow=uow,
#         user=user
#     )

#     return login_response

# @router.post('/logout')
# async def logout_user(
#     uow: UnitOfWork = Depends(UnitOfWork),
#     account = Depends(get_current_account)
# ):
#     await AccountService.logout(uow=uow, account_id=account.id)
#     return
