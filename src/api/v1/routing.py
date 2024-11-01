from fastapi import APIRouter
from api.v1.auth.routing.auth import router as auth_router

router = APIRouter(prefix='/v1')
router.include_router(auth_router)
