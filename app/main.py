from fastapi import FastAPI
from app.routes.ai import router as instant_router
from app.routes.ai_async import router as async_router


def create_app() -> FastAPI:
    app = FastAPI(title="Cobox AI", version="1.0.0")

    @app.get("/")
    def root():
        return {"message": "Cobox AI live - Dev"}

    @app.get("/health")
    def health():
        return {"status": "ok v1.0.0"}

    app.include_router(instant_router)
    app.include_router(async_router)

    return app
