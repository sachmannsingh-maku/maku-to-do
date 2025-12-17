from fastapi import FastAPI
from .router import router
from .middleware.logger import log_requests
from .exceptions import global_exception_handler

def create_app() -> FastAPI:
    app = FastAPI(title="Auth Service")

    app.include_router(router)
    app.middleware('http')(log_requests)
    app.add_exception_handler(Exception,global_exception_handler)

    return app
