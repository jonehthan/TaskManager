from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Create database start a session
database_filename = "task_management.db"
engine = create_engine(f"sqlite:///{database_filename}", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    """Initialize the database and create all tables"""
    Base.metadata.create_all(bind=engine)
