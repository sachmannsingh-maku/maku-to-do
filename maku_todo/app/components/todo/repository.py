from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Todo

async def create_todo_in_db(db : AsyncSession, title:str, description : str | None, owner_id : int) -> Todo:
    new_todo = Todo(title = title, description = description, owner_id = owner_id )
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo

async def get_todos_by_user(db : AsyncSession, owner_id : int) -> list[Todo]:
    todos = await db.execute(
        select(Todo).where(Todo.owner_id == owner_id)
    )
    return todos.scalars().all()

async def get_todo_by_id(db : AsyncSession, id : int) -> Todo:
    todos = await db.execute(
        select(Todo).where(Todo.id == id)
    )
    return todos.scalar_one_or_none()

async def delete_todos(db : AsyncSession, todo : Todo) -> Todo:
    await db.delete(todo)
    await db.commit()