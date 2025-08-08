# backend/init_db.py
import asyncio
from backend.database.session import engine
from backend.database.session import Base

async def init_db():
    async with engine.begin() as conn:
        # создаём все таблицы, если их ещё нет
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Таблицы успешно созданы в БД")

if __name__ == "__main__":
    asyncio.run(init_db())
