from fastapi import FastAPI
from src.api.v1.routers import router as api_v1_router


def init_app():
    app = FastAPI(docs_url="/api/v1/docs")
    app.include_router(api_v1_router)
    return app
