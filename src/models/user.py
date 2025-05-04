from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.database.db_config import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    tasks = relationship("Task", back_populates="user")
    
    def __repr__(self):
        return f"<User(ID='{self.id}', Username='{self.username}', Password={self.password})>"