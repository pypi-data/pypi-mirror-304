from fastapi import APIRouter

from jam.src.apps.routers.user import user_router
from jam.src.apps.routers.permission import permission_router
from jam.src.apps.routers.pulsar_manage import pulsar_router

from jam.src.settings import settings

if settings.API_PREFIX:
    base_url = f"/{settings.API_PREFIX}"
else:
    base_url = ""


router = APIRouter(prefix=base_url)

router.include_router(user_router, tags=["用户"], prefix='/user')
router.include_router(permission_router, tags=["权限"], prefix='/permission')
router.include_router(pulsar_router, tags=["操作"], prefix='/pulsar')
