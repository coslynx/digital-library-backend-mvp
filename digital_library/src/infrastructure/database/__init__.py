from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.config import settings
from infrastructure.database.models import Base

# Initialize the database engine using the connection URL from config.py
engine = create_engine(settings.DATABASE_URL)

# Create a session factory to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables based on the models defined in models/__init__.py
def initialize_database():
    Base.metadata.create_all(bind=engine)