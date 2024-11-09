from fastapi import APIRouter

from src.api.v1.post.views import router as post_router
from src.api.v1.review.views import router as review_router
from src.api.v1.user_auth.views import router as user_auth_router
from src.api.v1.user_profile.views import router as user_profile_router

router = APIRouter()

router.include_router(post_router, prefix="/post", tags=["Post"])
router.include_router(user_auth_router, prefix="/user_auth", tags=["UserAuth"])
router.include_router(review_router, prefix="/review", tags=["Review"])
router.include_router(user_profile_router, prefix="/user_profile", tags=["UserProfile"])
