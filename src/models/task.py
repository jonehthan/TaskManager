from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database.db_config import Base


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String, nullable=False)
    date = Column(Date)
    priority = Column(String)
    status = Column(String, nullable=False)
    completed_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(ID='{self.id}', User_id='{self.user_id}', Description={self.description})>"