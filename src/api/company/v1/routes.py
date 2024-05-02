from fastapi import APIRouter, Depends, Request

from src.core.utils import UnitOfWork
from src.api.auth.v1.middleware import AuthMiddleware


router: APIRouter = APIRouter(
    prefix='/v1/company',
    tags=['v1', 'company']
)



@router.post('/add-member', tags=['protected'])
async def add_new_member(
    request: Request,
    uow: UnitOfWork = Depends(UnitOfWork),
):
    payload: dict = request.state.payload
    company_id: int = payload['company_id']
    return company_id
