from fastapi import FastAPI

from src.api.v1.routers import router as api_v1_router
from src.infrastructure.redis import lifespan


def init_app():
    app = FastAPI(docs_url="/api/v1/docs", lifespan=lifespan)
    app.include_router(api_v1_router)
    return app
