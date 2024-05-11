from fastapi import APIRouter

from src.api.auth.v1.routers.auth_router import router as auth_router
from src.api.auth.v1.routers.register_router import router as register_router


router: APIRouter = APIRouter(
    prefix='/v1',
    tags=['v1']
)

router.include_router(auth_router)
router.include_router(register_router)
