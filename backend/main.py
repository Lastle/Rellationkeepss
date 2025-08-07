import os  
import asyncio  
from pathlib import Path  
from contextlib import asynccontextmanager, suppress  
from dotenv import load_dotenv  
from fastapi import FastAPI  
  
from tasks.reminder_checker import start_reminder_loop  
from backend.database.models import Base  
from backend.database.session import engine  
from backend.controllers import users, auth, reminders  
from backend.controllers import user_controller  

env_path = Path(__file__).parent.parent / ".env"  
load_dotenv(dotenv_path=env_path)  

  
@asynccontextmanager  
async def lifespan(app: FastAPI):  
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)  
        task = asyncio.create_task(start_reminder_loop())  
    try:  
        yield  
    finally:  
        task.cancel()  
        with suppress(asyncio.CancelledError):  
            await task  
  
app = FastAPI(lifespan=lifespan)  
app.include_router(user_controller.router)  
app.include_router(users.router, prefix="/users", tags=["users"])  
app.include_router(auth.router, prefix="/auth", tags=["auth"])  
app.include_router(reminders.router, prefix="/reminders", tags=["reminders"])  
  
@app.get("/")  
async def root():  
    return {"message": "Backend is running!"}  