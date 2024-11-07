from fastapi import APIRouter

from src.api.v1.post.views import router as post_router
from src.api.v1.user_auth.views import router as user_auth_router

router = APIRouter()

router.include_router(post_router, prefix="/post", tags=["Post"])
router.include_router(user_auth_router, prefix="/user_auth", tags=["UserAuth"])
