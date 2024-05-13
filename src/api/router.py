import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.db import get_async_session

from src.api.company.v1.routers import router as v1_company_router
from src.api.auth.v1.routers import router as v1_auth_router


router: APIRouter = APIRouter(
    prefix='/api'
)
router.include_router(v1_auth_router)
router.include_router(v1_company_router)


@router.get('/healthz/', tags=['healthz'])
async def health_check(session: AsyncSession = Depends(get_async_session)):
    async def check_service(service: str):
        try:
            if service == 'postgres':
                await session.execute(text('SELECT 1'))
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='PostgreSQL connection failed'
            )

    await asyncio.gather(*[
        check_service('postgres'),
    ])

    return JSONResponse(
        status_code=200,
        content={}
    )
