import os  
import httpx  
from dotenv import load_dotenv  
from pathlib import Path  
import aiohttp
env_path = Path(__file__).parent.parent / ".env"  
load_dotenv(dotenv_path=env_path)  
  
API_URL = os.getenv("BACKEND_URL", "http://localhost:8001")  
TOKEN_STORAGE = {}  
  
async def register_user(telegram_id: int, username: str = None, full_name: str = None) -> bool:  
    payload = {"telegram_id": telegram_id, "username": username, "full_name": full_name}  
    async with httpx.AsyncClient() as client:  
        try:  
            resp = await client.post(f"{API_URL}/users/register", json=payload)  
            if resp.status_code in (200, 201):  
                login_resp = await client.post(f"{API_URL}/auth/login", json={"telegram_id": telegram_id})  
                if login_resp.status_code == 200:  
                    token = login_resp.json()["access_token"]  
                    TOKEN_STORAGE[telegram_id] = token  
                    return True  
            elif resp.status_code == 409:  
                login_resp = await client.post(f"{API_URL}/auth/login", json={"telegram_id": telegram_id})  
                if login_resp.status_code == 200:  
                    token = login_resp.json()["access_token"]  
                    TOKEN_STORAGE[telegram_id] = token  
                    return True  
            return False  
        except httpx.HTTPError:  
            return False  
  
async def get_token(telegram_id: int) -> str | None:  
    return TOKEN_STORAGE.get(telegram_id)  
  
async def list_reminders(telegram_id: int):  
    token = await get_token(telegram_id)  
    if not token:  
        return []  
    headers = {"Authorization": f"Bearer {token}"}  
    async with httpx.AsyncClient() as client:  
        resp = await client.get(f"{API_URL}/reminders/", headers=headers)  
        if resp.status_code == 200:  
            return resp.json()  
        return []  
  
async def add_reminder(telegram_id: int, contact_name: str, message: str, remind_at: str) -> int | None:  
    token = await get_token(telegram_id)  
    if not token:  
        print("Нет токена для пользователя", telegram_id)  
        return None  
    headers = {"Authorization": f"Bearer {token}"}  
    payload = {  
        "contact_name": contact_name,  
        "message": message,  
        "remind_at": remind_at  
    }  
    try:  
        async with aiohttp.ClientSession() as session:  
            async with session.post(  
                "http://localhost:8001/reminders/",   # <-- укажи свой адрес!  
                headers=headers,  
                json=payload  
            ) as resp:  
                print("Ответ сервера:", resp.status)  
                try:  
                    data = await resp.json()  
                except Exception:  
                    data = await resp.text()  
                print("Тело ответа:", data)  
                if resp.status == 201 and isinstance(data, dict):  
                    return data.get("id")  
                return None  
    except Exception as e:  
        print("Ошибка при обращении к API:", e)  
        return None  
  
async def commit_reminder(telegram_id: int, reminder_id: int) -> bool:  
    token = await get_token(telegram_id)  
    if not token:  
        return False  
    headers = {"Authorization": f"Bearer {token}"}  
    async with httpx.AsyncClient() as client:  
        resp = await client.post(f"{API_URL}/reminders/{reminder_id}/commit", headers=headers)  
        return resp.status_code == 200  
  
async def delete_draft_reminder(telegram_id: int, reminder_id: int) -> bool:  
    token = await get_token(telegram_id)  
    if not token:  
        return False  
    headers = {"Authorization": f"Bearer {token}"}  
    async with httpx.AsyncClient() as client:  
        resp = await client.delete(f"{API_URL}/reminders/{reminder_id}/draft", headers=headers)  
        return resp.status_code == 204  