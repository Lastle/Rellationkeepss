from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey  
from backend.database.session import Base  
  
class Reminder(Base):  
    __tablename__ = "reminders"  
    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey("users.id"))  
    contact_name = Column(String)  
    remind_at = Column(DateTime)  # <-- вот так!  
    message = Column(String)  
    is_sent = Column(Boolean, default=False)  
    is_draft = Column(Boolean, default=True)  