from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select  
from backend.models.user import User  
from backend.database.session import get_db  
from backend.schemas.user import UserCreate, UserOut  
  
router = APIRouter()  
  
@router.post("/register", response_model=UserOut)  
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):  
    result = await db.execute(select(User).where(User.telegram_id == user.telegram_id))  
    existing_user = result.scalars().first()  
    if existing_user:  
        raise HTTPException(status_code=409, detail="User already exists")  
  
    new_user = User(  
        telegram_id=user.telegram_id,  
        username=user.username,  
        full_name=user.full_name  
    )  
    db.add(new_user)  
    await db.commit()  
    await db.refresh(new_user)  
    return new_user  