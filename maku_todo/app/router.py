from fastapi import APIRouter
from .components.system.controller import router as system_router
from .components.auth.controller import router as auth_router
from .components.todo.controller import router as todo_router
router = APIRouter()

router.include_router(system_router)
router.include_router(auth_router)
router.include_router(todo_router)
