from aiogram import Router, types  
from aiogram.filters import Command  
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  
  
router = Router()  
  
@router.message(Command("menu"))  
async def show_menu(message: types.Message):  
    keyboard = ReplyKeyboardMarkup(  
        keyboard=[  
            [KeyboardButton(text="/add"), KeyboardButton(text="/list")],  
            [KeyboardButton(text="/help")]  
        ],  
        resize_keyboard=True  
    )  
    await message.answer("📋 Главное меню:", reply_markup=keyboard)  
  
@router.message(Command("help"))  
async def help_handler(message: types.Message):  
    await message.answer(  
        "Доступные команды:\n"  
        "/add — добавить напоминание\n"  
        "/list — список ваших напоминаний\n"  
        "/menu — главное меню\n"  
        "/help — справка"  
    )  