import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from infrastructure.config import settings
from api.v1.schemas.book import Book, BookCreate, BookResponse
from tests.utils.auth import get_test_user, get_test_user_credentials
from tests.utils.utils import get_test_client


@pytest.fixture(scope="module")
def client():
    return get_test_client()


@pytest.fixture(scope="module")
def test_user(client: TestClient):
    return get_test_user(client)


@pytest.fixture(scope="function")
def db():
    with get_db() as db:
        yield db


def test_create_book(client: TestClient, db: Session, test_user: UserResponse):
    book_data = BookCreate(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        genre="Science Fiction",
        description="A humorous science fiction novel",
        publication_date="1979-05-12",
        cover_image="https://example.com/cover_image.jpg",
    )
    response = client.post(
        "/books",
        json=book_data.dict(),
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == book_data.title


def test_get_books(client: TestClient, db: Session, test_user: UserResponse):
    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_book(client: TestClient, db: Session, test_user: UserResponse):
    book_data = BookCreate(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        genre="Science Fiction",
        description="A humorous science fiction novel",
        publication_date="1979-05-12",
        cover_image="https://example.com/cover_image.jpg",
    )
    response = client.post(
        "/books",
        json=book_data.dict(),
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    book_id = response.json()["id"]

    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == book_data.title


def test_update_book(client: TestClient, db: Session, test_user: UserResponse):
    book_data = BookCreate(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        genre="Science Fiction",
        description="A humorous science fiction novel",
        publication_date="1979-05-12",
        cover_image="https://example.com/cover_image.jpg",
    )
    response = client.post(
        "/books",
        json=book_data.dict(),
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    book_id = response.json()["id"]

    updated_book_data = Book(
        title="The Restaurant at the End of the Universe",
        author="Douglas Adams",
        isbn="0345391802",
        genre="Science Fiction",
        description="A humorous science fiction novel",
        publication_date="1980-03-14",
        cover_image="https://example.com/cover_image.jpg",
    )
    response = client.put(
        f"/books/{book_id}",
        json=updated_book_data.dict(),
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == updated_book_data.title


def test_delete_book(client: TestClient, db: Session, test_user: UserResponse):
    book_data = BookCreate(
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        isbn="0345391802",
        genre="Science Fiction",
        description="A humorous science fiction novel",
        publication_date="1979-05-12",
        cover_image="https://example.com/cover_image.jpg",
    )
    response = client.post(
        "/books",
        json=book_data.dict(),
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    book_id = response.json()["id"]

    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND