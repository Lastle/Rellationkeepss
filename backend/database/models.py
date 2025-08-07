from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey  
from sqlalchemy.orm import relationship  
from backend.database.declarative_base import Base  
  
class User(Base):  
    __tablename__ = "users"  
  
    id = Column(Integer, primary_key=True, index=True)  
    telegram_id = Column(Integer, unique=True, index=True)  
    username = Column(String, nullable=True)  
    full_name = Column(String, nullable=True)  
    reminders = relationship("Reminder", back_populates="user")  
  
class Reminder(Base):  
    __tablename__ = "reminders"  
  
    id = Column(Integer, primary_key=True, index=True)  
    contact_name = Column(String, nullable=False)  
    remind_at = Column(DateTime, nullable=False)  
    message = Column(String, nullable=False)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    is_sent = Column(Boolean, default=False)  
    is_draft = Column(Boolean, default=True)  
  
    user = relationship("User", back_populates="reminders")  