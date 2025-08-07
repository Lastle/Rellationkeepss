from aiogram import Router, types, F  
from aiogram.filters import Command  
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton  
from aiogram.fsm.context import FSMContext  
from aiogram.fsm.state import State, StatesGroup  
from bot.api import list_reminders, add_reminder, commit_reminder, delete_draft_reminder  
import datetime  
  
router = Router()  
  
class ReminderFSM(StatesGroup):  
    waiting_for_message = State()  
    waiting_for_contact_name = State()  
    waiting_for_remind_at = State()  
    waiting_for_confirm = State()  
  
@router.message(Command("list"))  
async def cmd_list(message: types.Message):  
    reminders = await list_reminders(message.from_user.id)  
    if reminders:  
        text = "\n".join([  
            f"• <b>{r.get('message', '---')}</b> — <i>{r.get('remind_at', '').replace('T', ' ')}</i>"  
            for r in reminders  
        ])  
    else:  
        text = "Нет активных напоминаний."  
    await message.answer(text, parse_mode="HTML")  
  
@router.message(Command("add"))  
async def cmd_add(message: types.Message, state: FSMContext):  
    await message.answer("Введите текст напоминания:", reply_markup=ReplyKeyboardRemove())  
    await state.set_state(ReminderFSM.waiting_for_message)  
  
@router.message(ReminderFSM.waiting_for_message)  
async def process_message(message: types.Message, state: FSMContext):  
    await state.update_data(message_text=message.text)  
    await message.answer("Введите имя контакта для напоминания:")  
    await state.set_state(ReminderFSM.waiting_for_contact_name)  
  
@router.message(ReminderFSM.waiting_for_contact_name)  
async def process_contact_name(message: types.Message, state: FSMContext):  
    await state.update_data(contact_name=message.text)  
    await message.answer("Введите дату и время напоминания в формате ГГГГ-ММ-ДД ЧЧ:ММ")  
    await state.set_state(ReminderFSM.waiting_for_remind_at)  
  
@router.message(ReminderFSM.waiting_for_remind_at)  
async def process_remind_at(message: types.Message, state: FSMContext):  
    data = await state.get_data()  
    try:  
        dt = datetime.datetime.strptime(message.text, "%Y-%m-%d %H:%M")  
    except ValueError:  
        await message.answer("Неверный формат даты. Попробуйте ещё раз (ГГГГ-ММ-ДД ЧЧ:ММ):")  
        return  
  
    try:  
        reminder_id = await add_reminder(  
            message.from_user.id,  
            contact_name=data["contact_name"],  
            message=data["message_text"],  
            remind_at=dt.isoformat()  
        )  
    except Exception as e:  
        await message.answer(f"Ошибка при создании напоминания: {repr(e)}")  
        await state.clear()  
        return  
  
    if not reminder_id:  
        await message.answer("Ошибка: add_reminder вернул None или 0 (смотри логи сервера)")  
        await state.clear()  
        return  
  
    await state.update_data(reminder_id=reminder_id)  
    await message.answer(  
        f"Проверьте данные:\n"  
        f"Контакт: <b>{data['contact_name']}</b>\n"  
        f"Сообщение: <b>{data['message_text']}</b>\n"  
        f"Когда: <b>{dt}</b>\n\n"  
        "Подтвердить отправку? (да/нет)",  
        parse_mode="HTML"  
    )  
    await state.set_state(ReminderFSM.waiting_for_confirm)  
  
@router.message(ReminderFSM.waiting_for_confirm, F.text.lower() == "да")  
async def process_confirm(message: types.Message, state: FSMContext):  
    data = await state.get_data()  
    ok = await commit_reminder(message.from_user.id, data["reminder_id"])  
    if ok:  
        await message.answer("✅ Напоминание успешно создано!")  
    else:  
        await message.answer("Ошибка при подтверждении напоминания!")  
    await state.clear()  
  
@router.message(ReminderFSM.waiting_for_confirm, F.text.lower() == "нет")  
async def process_cancel(message: types.Message, state: FSMContext):  
    data = await state.get_data()  
    await delete_draft_reminder(message.from_user.id, data["reminder_id"])  
    await message.answer("❌ Напоминание отменено.")  
    await state.clear()  
  
@router.message(Command("menu"))  
async def cmd_menu(message: types.Message, state: FSMContext):  
    data = await state.get_data()  
    if "reminder_id" in data:  
        await delete_draft_reminder(message.from_user.id, data["reminder_id"])  
    await state.clear()  
    keyboard = ReplyKeyboardMarkup(  
        keyboard=[  
            [KeyboardButton(text="/add"), KeyboardButton(text="/list")],  
            [KeyboardButton(text="/help")]  
        ],  
        resize_keyboard=True  
    )  
    await message.answer("Вы вернулись в главное меню.", reply_markup=keyboard)  