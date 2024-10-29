from fastapi import APIRouter

from src.api.v1.post.views import router as post_router

router = APIRouter()

router.include_router(post_router, prefix="/post", tags=["Post"])
