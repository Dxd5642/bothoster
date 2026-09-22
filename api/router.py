from fastapi import APIRouter
from api.common import router as common_router
from api.v1.auth import router as auth_router
from api.v1.users import router as user_router


router = APIRouter(prefix="/api")

router.include_router(common_router)
router.include_router(auth_router)
router.include_router(user_router)