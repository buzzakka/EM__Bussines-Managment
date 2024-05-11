from fastapi import APIRouter

from src.api.company.v1.routers.member_router import router as member_router
from src.api.company.v1.routers.position_router import router as position_router
from src.api.company.v1.routers.struct_router import router as struct_router
from src.api.company.v1.routers.task_router import router as task_router


router: APIRouter = APIRouter(
    prefix='/v1/company',
    tags=['v1', 'company']
)

router.include_router(member_router)
router.include_router(position_router)
router.include_router(struct_router)
router.include_router(task_router)
