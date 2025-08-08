import asyncio  
from datetime import datetime  
from backend.database.session import AsyncSessionLocal  
from backend.models.reminder import Reminder  
from sqlalchemy.future import select  
  
async def send_reminder_message(reminder_id: int):  
    """  
    Асинхронная функция для отправки напоминания (background task).  
    """  
    async with AsyncSessionLocal() as session:  
        result = await session.execute(select(Reminder).where(Reminder.id == reminder_id))  
        reminder = result.scalar_one_or_none()  
        if not reminder:  
            print(f"Reminder with id={reminder_id} not found.")  
            return  
  
        # Твоя логика отправки (например, интеграция с ботом)  
        print(f"[Отправлено из фоновой задачи] Для user_id {reminder.user_id}: {reminder.message}")  
  
        reminder.is_sent = True  
        await session.commit()  
  
async def check_and_send_reminders():  
    """  
    Проверяет все неотправленные напоминания и отправляет их (например, раз в минуту).  
    """  
    async with AsyncSessionLocal() as session:  
        now = datetime.now()  
        result = await session.execute(  
            select(Reminder).where(  
                Reminder.remind_at <= now,  
                Reminder.is_sent == False,  
                Reminder.is_draft == False  
            )  
        )  
        reminders = result.scalars().all()  
        for reminder in reminders:  
            print(f"[Автосендер] user_id={reminder.user_id}: {reminder.message}")  
            # Можно сделать реальную отправку (например, await send_reminder_message(reminder.id))  
            reminder.is_sent = True  
        await session.commit()  
  
async def start_reminder_loop():  
    """  
    Запускает вечный цикл, каждую минуту проверяет и отправляет напоминания.  
    """  
    while True:  
        try:  
            await check_and_send_reminders()  
        except Exception as e:  
            print(f"Ошибка в reminder_loop: {e}")  
        await asyncio.sleep(60)  