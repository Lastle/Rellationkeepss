from fastapi import APIRouter, Depends, HTTPException, status  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select  
from pydantic import BaseModel  
from backend.database.session import get_db  
from backend.models.user import User   
from backend.services.security import create_access_token, get_current_user  
from backend.schemas.auth import Token  
  
router = APIRouter()  
  
class LoginRequest(BaseModel):  
    telegram_id: int  
  
@router.post("/login", response_model=Token)  
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):  
    result = await db.execute(select(User).where(User.telegram_id == data.telegram_id))  
    user = result.scalar_one_or_none()  
    if not user:  
        raise HTTPException(status_code=404, detail="User not found")  
  
    access_token = create_access_token(data={"sub": str(user.telegram_id)})  
    return {"access_token": access_token, "token_type": "bearer"}  
  
@router.get("/me")  
async def read_users_me(current_user: User = Depends(get_current_user)):  
    return {  
        "telegram_id": current_user.telegram_id,  
        "username": current_user.username,  
        "full_name": current_user.full_name,  
    }  