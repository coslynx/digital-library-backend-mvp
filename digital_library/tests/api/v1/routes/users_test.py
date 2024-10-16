import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from infrastructure.config import settings
from api.v1.schemas.user import User, UserCreate, UserResponse
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


def test_create_user(client: TestClient, db: Session):
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
    )
    response = client.post("/users", json=user_data.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_data.username


def test_get_users(client: TestClient, db: Session, test_user: UserResponse):
    response = client.get(
        "/users", headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_user(client: TestClient, db: Session, test_user: UserResponse):
    response = client.get(
        f"/users/{test_user['id']}", headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == test_user["username"]


def test_update_user(client: TestClient, db: Session, test_user: UserResponse):
    updated_user_data = User(
        username="updatedtestuser",
        email="updatedtestuser@example.com",
        password="testpassword",
    )
    response = client.put(
        f"/users/{test_user['id']}",
        json=updated_user_data.dict(),
        headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == updated_user_data.username


def test_delete_user(client: TestClient, db: Session, test_user: UserResponse):
    response = client.delete(
        f"/users/{test_user['id']}", headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(
        f"/users/{test_user['id']}", headers={"Authorization": f"Bearer {get_test_user_credentials(test_user)['access_token']}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND