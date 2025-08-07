from pydantic import BaseModel  
from typing import Optional  
  
class UserCreate(BaseModel):  
    telegram_id: int  
    username: Optional[str] = None  
    full_name: Optional[str] = None  
  
class UserOut(BaseModel):  
    telegram_id: int  
    username: Optional[str] = None  
    full_name: Optional[str] = None  
  
    class Config:  
        orm_mode = True  