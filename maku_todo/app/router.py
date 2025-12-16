from fastapi import APIRouter
from .components.system.controller import router as system_router

router = APIRouter()

router.include_router(system_router)
