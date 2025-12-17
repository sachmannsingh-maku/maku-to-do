from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from maku_todo.tasks.sample import sample
class SystemService:
    @staticmethod
    async def check_database(db: AsyncSession) -> bool:
        try:
            await db.execute(text("SELECT 1"))
            sample.delay("Hello")
            return True
        except Exception:
            return False
