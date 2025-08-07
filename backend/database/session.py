from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

