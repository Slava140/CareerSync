from fastapi import APIRouter

from api.v1.routing import router as api_v1_router

router = APIRouter(prefix='/api')
router.include_router(api_v1_router)