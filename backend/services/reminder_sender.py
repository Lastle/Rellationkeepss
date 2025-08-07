# Здесь интеграция с Telegram API (заглушка)  
import asyncio  
  
async def send_reminder_message(reminder_id: int):  
    print(f"[Reminder sender] Отправляем напоминание с id={reminder_id}")  
    await asyncio.sleep(1)  