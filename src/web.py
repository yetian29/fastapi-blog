from fastapi import FastAPI

from src.api.v1.routers import router as api_router


def init_app():
    app = FastAPI(docs_url="/api/v1/docs", debug=True)
    app.include_router(api_router)
    return app
