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

if __name__ == "__main__":
    create_database()