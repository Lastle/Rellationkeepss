from sqlalchemy import Column, Integer, String  
from backend.database.declarative_base import Base  

class User(Base):  
    __tablename__ = 'users'  
  
    id = Column(Integer, primary_key=True, index=True)  
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)  
    username = Column(String, index=True, nullable=True)  
    # добавь другие поля, если нужно  