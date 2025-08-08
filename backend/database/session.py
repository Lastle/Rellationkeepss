from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  
from sqlalchemy.orm import sessionmaker, declarative_base  
from sqlalchemy import create_engine  
import os  
from dotenv import load_dotenv  
  
load_dotenv()  
  
Base = declarative_base()  
DB_URL = os.getenv("DATABASE_URL")  
if not DB_URL:  
    raise ValueError("DATABASE_URL is not set in .env file")  
  
# ASYNC engine and session  
engine = create_async_engine(DB_URL, echo=True, future=True)  
AsyncSessionLocal = sessionmaker(  
    bind=engine,  
    expire_on_commit=False,  
    class_=AsyncSession,  
)  
  
# SYNC engine and session (for sync code)  
sync_engine = create_engine(DB_URL.replace('asyncpg', 'psycopg2'), echo=True, future=True)  
SessionLocal = sessionmaker(  
    bind=sync_engine,  
    expire_on_commit=False,  
)  
  
# Dependency for async session (FastAPI Depends)  
async def get_db():  
    async with AsyncSessionLocal() as session:  
        yield session  
  
# Dependency for sync session (if needed)  
def get_sync_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close()  