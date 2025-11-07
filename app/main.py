from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import settings
from app.api.routes import router as api_router
from app.db.session import init_engine_and_create


def create_app() -> FastAPI:
    app = FastAPI(title="Resume Assessment Agent", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_engine_and_create(settings.database_url)

    app.include_router(api_router, prefix="/v1")
    return app


app = create_app()


