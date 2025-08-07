import asyncio  
from datetime import datetime  
from sqlalchemy.future import select  
from backend.database.session import get_db  
from backend.database.models import Reminder  
from backend.services.reminder_sender import send_reminder_message  
  
async def start_reminder_loop():  
    while True:  
        async with get_db() as db:  
            now = datetime.utcnow()  
            result = await db.execute(  
                select(Reminder).where(Reminder.remind_at <= now, Reminder.is_sent == False, Reminder.is_draft == False)  
            )  
            reminders = result.scalars().all()  
            for reminder in reminders:  
                # TODO: интеграция с Telegram-ботом  
                await send_reminder_message(reminder.id)  
                reminder.is_sent = True  
            await db.commit()  
        await asyncio.sleep(60)  