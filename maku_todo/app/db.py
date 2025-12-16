from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from pydantic_settings import BaseSettings

from sqlalchemy.orm import sessionmaker, declarative_base

from typing import AsyncGenerator


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session