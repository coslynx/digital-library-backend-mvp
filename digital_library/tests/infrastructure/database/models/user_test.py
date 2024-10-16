import pytest
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from infrastructure.database.models import User, Book
from tests.utils.utils import get_test_database_url
from tests.utils.auth import get_test_user, get_test_user_credentials


@pytest.fixture(scope="module")
def engine():
    test_url = get_test_database_url()
    engine = create_engine(test_url)
    return engine


@pytest.fixture(scope="module")
def session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    return get_test_client()


@pytest.fixture(scope="module")
def test_user(client):
    return get_test_user(client)


def test_create_user(session: Session, test_user: User):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": "testpassword",
    }
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.hashed_password == user_data["hashed_password"]
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.borrowed_books == []


def test_get_user(session: Session, test_user: User):
    retrieved_user = session.query(User).filter(User.id == test_user.id).first()

    assert retrieved_user.id == test_user.id
    assert retrieved_user.username == test_user.username
    assert retrieved_user.email == test_user.email
    assert retrieved_user.hashed_password == test_user.hashed_password
    assert retrieved_user.created_at == test_user.created_at
    assert retrieved_user.updated_at == test_user.updated_at
    assert retrieved_user.borrowed_books == []


def test_update_user(session: Session, test_user: User):
    updated_user_data = {
        "username": "updatedtestuser",
        "email": "updatedtestuser@example.com",
        "hashed_password": "updatedtestpassword",
    }
    test_user.username = updated_user_data["username"]
    test_user.email = updated_user_data["email"]
    test_user.hashed_password = updated_user_data["hashed_password"]
    session.commit()
    session.refresh(test_user)

    assert test_user.username == updated_user_data["username"]
    assert test_user.email == updated_user_data["email"]
    assert test_user.hashed_password == updated_user_data["hashed_password"]


def test_delete_user(session: Session, test_user: User):
    session.delete(test_user)
    session.commit()

    retrieved_user = session.query(User).filter(User.id == test_user.id).first()
    assert retrieved_user is None