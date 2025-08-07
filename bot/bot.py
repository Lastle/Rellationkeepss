import logging  
import os  
import requests  
from aiogram import Bot, Dispatcher, types  
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  
from aiogram.filters import Command  
from aiogram import F  
from aiogram.fsm.storage.memory import MemoryStorage  
from dotenv import load_dotenv  
import asyncio  
  
load_dotenv()  
BOT_TOKEN = os.getenv("BOT_TOKEN")  
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")   
  
logging.basicConfig(level=logging.INFO)  
  
bot = Bot(token=BOT_TOKEN)  
dp = Dispatcher(storage=MemoryStorage())  
  
main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[  
    [KeyboardButton(text="Главное меню")]  
])  
  
@dp.message(Command("start"))  
async def start_handler(message: types.Message):  
    payload = {  
        "telegram_id": message.from_user.id,  
        "username": message.from_user.username or ""  
    }  
    try:  
        response = requests.post(  
            f"{BACKEND_URL}/register",  
            params=payload,  
            timeout=5  
        )  
        if response.status_code == 200:  
            await message.answer(  
                "Вы успешно зарегистрированы! 👋\nИспользуйте меню для продолжения.",  
                reply_markup=main_menu_kb  
            )  
        else:  
            await message.answer("Ошибка регистрации. Попробуйте позже.")  
    except Exception as e:  
        await message.answer("Не удалось связаться с сервером. Попробуйте позже.")  
  
@dp.message(F.text == "Главное меню")  
async def main_menu_handler(message: types.Message):  
    await message.answer(  
        "Вы в главном меню!\n(Здесь будут доступны ваши функции)",  
        reply_markup=main_menu_kb  
    )  
  
async def main():  
    await dp.start_polling(bot)  
  
if __name__ == "__main__":  
    asyncio.run(main())  