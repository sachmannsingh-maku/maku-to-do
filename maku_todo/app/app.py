from fastapi import FastAPI
from .router import router

def create_app() -> FastAPI:
    app = FastAPI(title="Auth Service")

    app.include_router(router)

    return app
