import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from infrastructure.config import settings
from api.v1.schemas.auth import Token, User, UserResponse
from tests.utils.auth import get_test_user, get_test_user_credentials
from tests.utils.utils import get_test_client
from utils.exceptions import AuthenticationError


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


def test_signup_user(client: TestClient, db: Session):
    """Test the signup endpoint."""
    new_user = User(username="testuser", password="testpassword")
    response = client.post("/auth/signup", json=new_user.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == new_user.username


def test_login_user(client: TestClient, test_user: UserResponse):
    """Test the login endpoint."""
    credentials = get_test_user_credentials(test_user)
    response = client.post("/auth/login", data=credentials)
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)


def test_login_user_invalid_credentials(client: TestClient):
    """Test the login endpoint with invalid credentials."""
    credentials = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/auth/login", data=credentials)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client: TestClient, test_user: UserResponse):
    """Test the refresh token endpoint."""
    credentials = get_test_user_credentials(test_user)
    login_response = client.post("/auth/login", data=credentials)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]
    refresh_response = client.post(
        "/auth/refresh_token", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert refresh_response.status_code == status.HTTP_200_OK
    assert refresh_response.json()["access_token"] == access_token


def test_refresh_token_invalid_token(client: TestClient):
    """Test the refresh token endpoint with an invalid token."""
    response = client.post("/auth/refresh_token", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED