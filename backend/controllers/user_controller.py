from fastapi import APIRouter, Depends  
from sqlalchemy.orm import Session  
from backend.models.user import User   
from backend.database.session import get_db   
  
router = APIRouter()  
  
@router.post('/register')  
def register_user(telegram_id: int, username: str, db: Session = Depends(get_db)):  
    user = db.query(User).filter_by(telegram_id=telegram_id).first()  
    if user:  
        return {"message": "User already registered"}  
    user = User(telegram_id=telegram_id, username=username)  
    db.add(user)  
    db.commit()  
    db.refresh(user)  
    return {"message": "User registered", "user_id": user.id}  