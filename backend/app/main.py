from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth as auth_router
from app.api.v1 import users as users_router
from app.api.v1 import jobs as jobs_router
from app.api.v1 import resumes as resumes_router
from app.api.v1 import ai as ai_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[*settings.CORS_ORIGINS] if settings.CORS_ORIGINS else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    api_prefix = settings.API_V1_STR
    app.include_router(auth_router.router, prefix=api_prefix)
    app.include_router(users_router.router, prefix=api_prefix)
    app.include_router(jobs_router.router, prefix=api_prefix)
    app.include_router(resumes_router.router, prefix=api_prefix)
    app.include_router(ai_router.router, prefix=api_prefix)

    return app


app = create_app()

