from fastapi import APIRouter

from src.api.company.v1.routers import router as v1_company_router
from src.api.auth.v1.routers import router as v1_auth_router


router: APIRouter = APIRouter(
    prefix='/api'
)
router.include_router(v1_auth_router)
router.include_router(v1_company_router)
