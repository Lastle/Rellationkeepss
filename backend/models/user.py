from sqlalchemy import Column, Integer, String  
from backend.database.session import Base  

class User(Base):  
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True, index=True)  
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)  
    username = Column(String, index=True, nullable=True)  