from src.database.db_config import session
from src.models.user import User
from src.models.task import Task

# Getters/Setters for database objects
class DatabaseManager:
    @staticmethod
    def add_user(username, password):
        if username and password:
            if not session.query(User).filter_by(username=username).first():
                user = User(username=username, password=password)
                session.add(user)
                session.commit()
                return user
        return None

    @staticmethod
    def login(username, password):
        if username and password:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user:
                return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_username(username):
        return session.query(User).filter_by(username=username).first()

    @staticmethod
    def get_all_users():
        return session.query(User).all()

    @staticmethod
    def update_username(user_id, username):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.username = username
            session.commit()
            return True
        return False

    @staticmethod
    def update_password(user_id, password):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.password = password
            session.commit()
            return True
        return False

    @staticmethod
    def delete_user(user_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

    @staticmethod
    def delete_all_users():
        session.query(User).delete()
        session.commit()

    @staticmethod
    def add_task(user_id, description, date, priority, status):
        task = Task(
            user_id=user_id,
            description=description,
            date=date,
            priority=priority,
            status=status
        )
        session.add(task)
        session.commit()
        return task

    @staticmethod
    def get_task_by_id(task_id):
        return session.query(Task).filter_by(id=task_id).first()

    @staticmethod
    def get_tasks_by_user_id(user_id):
        return session.query(Task).filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_tasks():
        return session.query(Task).all()

    @staticmethod
    def delete_task(task_id):
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()
            return True
        return False

    @staticmethod
    def update_task(task_id, description, date, priority, status, completed_date=None):
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            task.description = description
            task.date = date
            task.priority = priority
            task.status = status
            if completed_date:
                task.completed_date = completed_date
            session.commit()
            return True
        return False
