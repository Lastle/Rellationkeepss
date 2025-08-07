from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select  
from backend.database.models import Reminder, User  
from backend.database.session import get_db  
from backend.services.security import get_current_user  
from backend.services.reminder_sender import send_reminder_message  
from backend.schemas.reminder import ReminderCreate, ReminderOut  
  
router = APIRouter()  
  
@router.post("/", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)  
async def create_reminder(  
    reminder_data: ReminderCreate,  
    background_tasks: BackgroundTasks,  
    current_user: User = Depends(get_current_user),  
    db: AsyncSession = Depends(get_db),  
):  
    # Приводим remind_at к naive datetime (без tzinfo), если надо  
    remind_at = reminder_data.remind_at  
    if remind_at.tzinfo is not None:  
        remind_at = remind_at.replace(tzinfo=None)  
  
    reminder = Reminder(  
        user_id=current_user.id,  
        contact_name=reminder_data.contact_name,  
        remind_at=remind_at,  
        message=reminder_data.message,  
        is_sent=False,  
        is_draft=True,  
    )  
    db.add(reminder)  
    await db.commit()  
    await db.refresh(reminder)  
    return reminder  
  
@router.post("/{reminder_id}/commit", response_model=ReminderOut)  
async def commit_reminder(  
    reminder_id: int,  
    background_tasks: BackgroundTasks,  
    current_user: User = Depends(get_current_user),  
    db: AsyncSession = Depends(get_db)  
):  
    result = await db.execute(  
        select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == current_user.id)  
    )  
    reminder = result.scalar_one_or_none()  
    if not reminder:  
        raise HTTPException(status_code=404, detail="Reminder not found")  
    reminder.is_draft = False  
    await db.commit()  
    await db.refresh(reminder)  
    background_tasks.add_task(send_reminder_message, reminder.id)  
    return reminder  
  
@router.delete("/{reminder_id}/draft", status_code=status.HTTP_204_NO_CONTENT)  
async def delete_draft_reminder(  
    reminder_id: int,  
    current_user: User = Depends(get_current_user),  
    db: AsyncSession = Depends(get_db)  
):  
    result = await db.execute(  
        select(Reminder).where(  
            Reminder.id == reminder_id,  
            Reminder.user_id == current_user.id,  
            Reminder.is_draft == True  
        )  
    )  
    reminder = result.scalar_one_or_none()  
    if not reminder:  
        raise HTTPException(status_code=404, detail="Draft reminder not found")  
    await db.delete(reminder)  
    await db.commit()  
    return None  
  
@router.get("/", response_model=list[ReminderOut])  
async def get_reminders(  
    db: AsyncSession = Depends(get_db),  
    current_user: User = Depends(get_current_user)  
):  
    result = await db.execute(  
        select(Reminder).where(  
            Reminder.user_id == current_user.id,  
            Reminder.is_draft == False  
        )  
    )  
    reminders = result.scalars().all()  
    return reminders  