from fastapi import APIRouter

from src.api.auth.v1.routes import router as v1_routes


router: APIRouter = APIRouter(
    prefix='/auth/api'
)
router.include_router(v1_routes)
