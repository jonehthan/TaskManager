import sqlite3

from sqlalchemy import create_engine, Column, String, Float, Integer, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


database_filename = "task_management.db"
engine = create_engine(f"sqlite:///{database_filename}", echo=False)



Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    
    # Use ID as a string primary key
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    
    tasks = relationship("Task", back_populates="user")
    def __repr__(self):
        return f"<User(ID='{self.id}', Username='{self.username}', Password={self.password})>"

class Task(Base):
    __tablename__ = 'task'
    
    # Use ID as a string primary key
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String, nullable = False)
    date = Column(Date)
    category = Column(String)
    priority = Column(String)
    status = Column(String, nullable = False)

    user = relationship("User", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(ID='{self.id}', User_id='{self.user_id}', Description={self.description})>"

# Creating the tables
def create_db():
    Base.metadata.create_all(bind=engine)
    
Session = sessionmaker(bind=engine)
session = Session()

#User functions
def add_user(username, password):
    if username and password:
        if not session.query(User).filter_by(username = username).first():
            user = User(username = username, password = password)
            session.add(user)
            session.commit()
            return user
    return None

def login(username, password):
    if username and password:
        user = session.query(User).filter_by(username = username, password = password).first()
        if user:
            return user
    return None

def get_user_id(user_id):
    user = session.query(User).filter_by(id = user_id).first()
    return user

def get_user_username(username):
    user = session.query(User).filter_by(username = username).first()
    return user

def get_users():
    users = session.query(User).all()
    return users

def update_username(user_id, username):
    user = session.query(User).filter_by(id = user_id).first()
    if user:
        user.username = username
    session.commit()

def update_password(user_id, password):
    user = session.query(User).filter_by(id = user_id).first()
    if user:
        user.password = password
    session.commit()

def delete_user(user_id):
    user = session.query(User).filter_by(id = user_id).first()
    session.delete(user)
    session.commit()

def delete_all_users():
    session.query(User).delete()
    session.commit()

#Task functions
def add_task(user_id, description, date, category, priority, status):
    task = Task(user_id = user_id, description = description,  date = date, category = category, priority = priority, status = status)
    session.add(task)
    session.commit()
    print("Added task: " + str(task))

def get_task_id(task_id):
    task = session.query(Task).filter_by(id = task_id).first()
    return task

def get_tasks_user_id(user_id):
    tasks = session.query(Task).filter_by(user_id = user_id).all()
    return tasks

def get_tasks():
    tasks = session.query(Task).all()
    return tasks

def delete_task(task_id):
    deleted_task = session.query(Task).filter_by(id = task_id).first()
    if deleted_task:
        session.delete(deleted_task)
        session.commit()
    else:
        print("Task not found")
    
def update_task(task_id, task_description, task_date, task_category, task_priority, task_status):
    task = session.query(Task).filter_by(id = task_id).first()
    if task:
        task.description = task_description
        task.date = task_date
        task.category = task_category
        task.priority = task_priority
        task.status = task_status
    session.commit()

def display_tasks():
    tasks = session.query(Task).all()
    for task in tasks:
        print(task.id, task.description, task.date, task.category, task.priority, task.status)
