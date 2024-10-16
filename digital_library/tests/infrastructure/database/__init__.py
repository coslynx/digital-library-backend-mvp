import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.config import settings
from infrastructure.database.models import Base, User, Book
from tests.utils.utils import get_test_database_url

# This file tests the database initialization and model interactions.
# It ensures that the database is set up correctly and that model
# interactions with the database function as expected.

@pytest.fixture(scope="module")
def engine():
    """Creates a test database engine."""
    test_url = get_test_database_url()
    engine = create_engine(test_url)
    return engine

@pytest.fixture(scope="module")
def session(engine):
    """Creates a test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def base():
    """Creates a test base class for models."""
    Base = declarative_base()
    return Base

def test_database_initialization(engine, base):
    """Tests database initialization and table creation."""
    Base.metadata.create_all(bind=engine)
    # Verify table creation (add your specific table verification logic here)
    # ...
    Base.metadata.drop_all(bind=engine)

def test_user_model_interaction(session):
    """Tests interactions with the User model."""
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="testpassword",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"

    session.delete(user)
    session.commit()

def test_book_model_interaction(session):
    """Tests interactions with the Book model."""
    book = Book(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        genre="Science Fiction",
        publication_date="1979-05-12",
    )
    session.add(book)
    session.commit()
    session.refresh(book)

    assert book.id is not None
    assert book.title == "The Hitchhiker's Guide to the Galaxy"

    session.delete(book)
    session.commit()