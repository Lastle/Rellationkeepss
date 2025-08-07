from pydantic import BaseModel  
from datetime import datetime  
  
class ReminderCreate(BaseModel):  
    contact_name: str  
    remind_at: datetime  
    message: str  
  
class ReminderOut(BaseModel):  
    id: int  
    contact_name: str  
    remind_at: datetime  
    message: str  
    user_id: int  
    is_sent: bool  
    is_draft: bool  
  
    class Config:  
        orm_mode = True  # Важно! чтобы Pydantic знал, что это ORM-объект  