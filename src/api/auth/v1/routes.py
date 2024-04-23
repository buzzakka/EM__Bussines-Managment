from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr

from src.api.auth.v1.models.invite import InviteModel
from src.api.auth.v1.schemas.user import SignUpRequestSchema
from src.api.auth.v1.services.invite import InviteService
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

    if user is not None:
        raise HTTPException(status_code=400, detail='Пользователь уже зарегестрирован.')

    invite = await InviteService.create_invite_token(uow=uow, email=account)

    return invite


@router.post(
    path='/sign-up-complete',
)
async def sign_up_complete(
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

    return db_token
