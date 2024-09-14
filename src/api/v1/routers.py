from fastapi import APIRouter

from src.api.v1.post.views import router as post_router
from src.api.v1.review.views import router as review_router
from src.api.v1.user_auth.views import router as user_router

router = APIRouter()


router.include_router(post_router, prefix="/post", tags=["post"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(review_router, prefix="/review", tags=["review"])
