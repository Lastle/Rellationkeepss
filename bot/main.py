import asyncio  
import os  
from pathlib import Path  
from aiogram import Bot, Dispatcher  
from aiogram.fsm.storage.memory import MemoryStorage  
from aiogram.client.bot import DefaultBotProperties  
from dotenv import load_dotenv  
  
env_path = Path(__file__).parent.parent / ".env"  
load_dotenv(dotenv_path=env_path)  
  
TOKEN = os.getenv("BOT_TOKEN")  
if not TOKEN:  
    raise ValueError("BOT_TOKEN is not set in .env")  
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))  
dp = Dispatcher(storage=MemoryStorage())  
  
from bot.handlers.menu import router as menu_router  
from bot.handlers.registration import router as reg_router  
from bot.handlers.reminders import router as rem_router  
  
dp.include_router(reg_router)  
dp.include_router(menu_router)  
dp.include_router(rem_router)  
  
async def main():  
    print("🤖 Bot is starting...")  
    await dp.start_polling(bot)  
  
if __name__ == "__main__":  
    asyncio.run(main())  