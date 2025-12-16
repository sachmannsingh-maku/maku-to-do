from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_db
from maku_todo.app.components.auth.dependency import get_current_user
from .schemas import TodoCreate, TodoUpdate, TodoResponse
from .service import (
    create_todo_service,
    list_todos_service,
    update_todo_service,
    delete_todo_service,
)

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate,db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    return await create_todo_service(db, current_user, todo)


@router.get("/", response_model=list[TodoResponse])
async def list_todos(db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    return await list_todos_service(db, current_user)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int,todo: TodoUpdate,db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    return await update_todo_service(db, todo_id, todo, current_user)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int,db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    await delete_todo_service(db, todo_id, current_user)