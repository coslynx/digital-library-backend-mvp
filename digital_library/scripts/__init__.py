from infrastructure.config import settings
from infrastructure.database.db_session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the base model for SQLAlchemy
Base = declarative_base()

def create_database():
    """
    Creates the PostgreSQL database specified in the environment variables.

    This function connects to the PostgreSQL database and creates the database
    if it doesn't already exist. It utilizes the `DATABASE_URL` environment
    variable to get the connection string.
    """
    # Get the database connection URL from environment variables
    database_url = settings.DATABASE_URL

    # Create a SQLAlchemy engine using the provided URL
    engine = create_engine(database_url)

    # Create the database if it doesn't exist
    if not engine.dialect.has_table(engine, settings.POSTGRES_DB):
        engine.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")

def seed_users(db: sessionmaker):
    """
    Seeds the database with initial user data.

    Args:
        db: A SQLAlchemy session object.
    """
    for user_data in users:
        db_user = User(**user_data)
        db.add(db_user)
    db.commit()

def seed_books(db: sessionmaker):
    """
    Seeds the database with initial book data.

    Args:
        db: A SQLAlchemy session object.
    """
    for book_data in books:
        db_book = Book(**book_data)
        db.add(db_book)
    db.commit()

if __name__ == "__main__":
    with get_db() as db:
        seed_users(db)
        seed_books(db)