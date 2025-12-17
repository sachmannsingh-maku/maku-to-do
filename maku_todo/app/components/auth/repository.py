from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User

async def get_user_by_email(self,db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    u = result.scalar_one_or_none()
    return u

async def get_user_by_id(self,db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def create_user(self,db: AsyncSession, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
