from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr

from src.core.utils.unit_of_work import UnitOfWork
from src.api.auth.v1.services.registration import RegistrationService
from src.api.auth.v1.services.account import AccountService
from src.api.auth.v1.services.invite import InviteService
from src.api.auth.v1.models.invite import InviteModel
from src.api.auth.v1.models.account import AccountModel
from src.api.auth.v1.schemas.user import SignUpCompleteRequestSchema, SignUpRequestSchema, UserLoginSchema
from src.api.auth.v1.exceptions import RegistrationError


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
    account_obj: AccountModel = await AccountService.get_by_query_one_or_none(uow=uow, email=account)

    if account_obj is not None:
        raise HTTPException(status_code=400, detail='Пользователь уже зарегестрирован.')

    invite = await InviteService.create_invite_token(uow=uow, email=account)

    return invite


@router.post(
    path='/sign-up',
)
async def sign_up(
    info: SignUpRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    db_token: InviteModel = await InviteService.get_by_query_one_or_none(
        uow, 
        email=info.account,
        token=info.invite_token
    )

    if db_token is None:
        raise HTTPException(status_code=400, detail='Некорректные данные.')

    db_token: InviteModel = await InviteService.update_one_by_id(uow=uow, _id=db_token.id, values={'is_confirmed': True})

    return {'status': 'success', 'email': info.account}


@router.post(
    path='/sign-up-complete'
)
async def sign_up_complete(
    user_data: SignUpCompleteRequestSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    try:
        await RegistrationService.register_user(uow=uow, user_data=user_data.model_dump())
    except RegistrationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    return


@router.post('/login')
async def auth_user(
    user: UserLoginSchema
):
  async with UnitOfWork():
    AccountService.add_one(UnitOfWork, email='qew@qwe.ru')
    AccountService.add_one(UnitOfWork, email='qew1@qwe.ru')
    # raise
    AccountService.add_one(UnitOfWork, email='qew@qwe2.ru')
