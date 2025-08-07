from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Я помогу тебе не забывать о важных людях.\n\nЧтобы продолжить, нажми кнопку ниже.")