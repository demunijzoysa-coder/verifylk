from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router as api_router
from .config import get_settings
from .middleware.audit import audit_middleware


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(audit_middleware)

    @app.get("/", summary="Root")
    def root():
        return {"message": "VerifyLK API", "environment": settings.environment}

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
