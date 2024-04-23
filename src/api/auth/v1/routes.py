from fastapi import APIRouter
from pydantic import EmailStr

router: APIRouter = APIRouter(
    prefix='/v1',
    tags=['v1']
)


@router.get(
    path='/check_account/{account}'
)
async def check_account(
    account: EmailStr,
):
    return
