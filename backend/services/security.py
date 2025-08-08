import os  
from datetime import datetime, timedelta  
from typing import Optional  
  
from jose import JWTError, jwt  
from passlib.context import CryptContext  
from fastapi import Depends, HTTPException, status  
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select  
from backend.database.session import get_db  
from backend.models.user import User 
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  
  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  
bearer_scheme = HTTPBearer()  
  
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):  
    to_encode = data.copy()  
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))  
    to_encode.update({"exp": expire})  
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return encoded_jwt  
  
async def get_current_user(  
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  
    db: AsyncSession = Depends(get_db)  
) -> User:  
    token = credentials.credentials  
    try:  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        telegram_id = payload.get("sub")  
        if telegram_id is None:  
            raise HTTPException(status_code=401, detail="Invalid token")  
        result = await db.execute(select(User).where(User.telegram_id == int(telegram_id)))  
        user = result.scalars().first()  
        if user is None:  
            raise HTTPException(status_code=401, detail="User not found")  
        return user  
    except JWTError:  
        raise HTTPException(status_code=401, detail="Invalid token")  