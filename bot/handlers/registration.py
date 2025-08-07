from aiogram import Router, types  
from aiogram.filters import Command  
from bot.api import register_user  
  
router = Router()  
  
@router.message(Command("start"))  
async def start_registration(message: types.Message):  
    user = message.from_user  
    registered = await register_user(  
        telegram_id=user.id,  
        username=user.username,  
        full_name=user.full_name  
    )  
    if registered:  
        await message.answer("✅ Вы зарегистрированы!\nНажмите /menu для начала работы.")  
    else:  
        await message.answer("❌ Ошибка регистрации. Попробуйте позже.")  