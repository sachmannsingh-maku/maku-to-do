from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import *

async def create_todo_service(db:AsyncSession, current_user, todoData):
    return await create_todo_in_db(db, title = todoData.title, description = todoData.description, owner_id = current_user.id)

async def list_todos_service(db:AsyncSession, current_user):
    return await get_todos_by_user(db, owner_id = current_user.id)

async def get_todo_or_404(db:AsyncSession, todo_id:int):
    res = await get_todo_by_id(db,todo_id)
    if res is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "requested Todo Not Found")
    return res

def verify_ownership(todo:Todo, current_user):
    if(todo.owner_id != current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= "Not authorized to access this todo")
    
async def update_todo_service(db:AsyncSession, todo_id:int, todo_data, current_user):
    todo = await get_todo_or_404(db, todo_id)
    verify_ownership(todo, current_user)

    for field, value in todo_data.model_dump(exclude_unset=True).items():
        if field == 'completed':
            value = eval(value.capitalize())
        setattr(todo, field, value)
    
    await db.commit()
    await db.refresh(todo)
    return todo

async def delete_todo_service(db: AsyncSession, todo_id: int, current_user,):
    todo = await get_todo_or_404(db, todo_id)
    verify_ownership(todo, current_user)
    await delete_todos(db, todo)
