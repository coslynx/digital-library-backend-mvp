import pytest
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from infrastructure.database.models import Book, User
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


def test_create_book(session: Session, test_user: User):
    book_data = {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "isbn": "0345391802",
        "genre": "Science Fiction",
        "description": "A humorous science fiction novel",
        "publication_date": "1979-05-12",
        "cover_image": "https://example.com/cover_image.jpg",
    }
    book = Book(**book_data)
    session.add(book)
    session.commit()
    session.refresh(book)

    assert book.id is not None
    assert book.title == book_data["title"]
    assert book.author == book_data["author"]
    assert book.isbn == book_data["isbn"]
    assert book.genre == book_data["genre"]
    assert book.description == book_data["description"]
    assert book.publication_date == book_data["publication_date"]
    assert book.cover_image == book_data["cover_image"]
    assert book.is_available is True
    assert book.borrower_id is None

    # Check book association with user
    user = session.query(User).filter(User.id == test_user["id"]).first()
    assert user.borrowed_books == []


def test_get_book(session: Session, test_user: User):
    book_data = {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "isbn": "0345391802",
        "genre": "Science Fiction",
        "description": "A humorous science fiction novel",
        "publication_date": "1979-05-12",
        "cover_image": "https://example.com/cover_image.jpg",
    }
    book = Book(**book_data)
    session.add(book)
    session.commit()
    session.refresh(book)

    retrieved_book = session.query(Book).filter(Book.id == book.id).first()

    assert retrieved_book.id == book.id
    assert retrieved_book.title == book.title
    assert retrieved_book.author == book.author
    assert retrieved_book.isbn == book.isbn
    assert retrieved_book.genre == book.genre
    assert retrieved_book.description == book.description
    assert retrieved_book.publication_date == book.publication_date
    assert retrieved_book.cover_image == book.cover_image
    assert retrieved_book.is_available is True
    assert retrieved_book.borrower_id is None


def test_update_book(session: Session, test_user: User):
    book_data = {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "isbn": "0345391802",
        "genre": "Science Fiction",
        "description": "A humorous science fiction novel",
        "publication_date": "1979-05-12",
        "cover_image": "https://example.com/cover_image.jpg",
    }
    book = Book(**book_data)
    session.add(book)
    session.commit()
    session.refresh(book)

    updated_book_data = {
        "title": "The Restaurant at the End of the Universe",
        "author": "Douglas Adams",
        "isbn": "0345391802",
        "genre": "Science Fiction",
        "description": "A humorous science fiction novel",
        "publication_date": "1980-03-14",
        "cover_image": "https://example.com/cover_image.jpg",
    }
    book.title = updated_book_data["title"]
    book.publication_date = updated_book_data["publication_date"]
    session.commit()
    session.refresh(book)

    assert book.title == updated_book_data["title"]
    assert book.publication_date == updated_book_data["publication_date"]


def test_delete_book(session: Session, test_user: User):
    book_data = {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "isbn": "0345391802",
        "genre": "Science Fiction",
        "description": "A humorous science fiction novel",
        "publication_date": "1979-05-12",
        "cover_image": "https://example.com/cover_image.jpg",
    }
    book = Book(**book_data)
    session.add(book)
    session.commit()
    session.refresh(book)

    session.delete(book)
    session.commit()

    retrieved_book = session.query(Book).filter(Book.id == book.id).first()
    assert retrieved_book is None