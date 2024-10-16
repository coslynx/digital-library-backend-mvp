from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from infrastructure.config import settings
from infrastructure.database.db_session import get_db
from utils.auth import create_access_token, create_refresh_token, verify_password, get_current_user
from api.v1.schemas.auth import Token, User, UserResponse

from infrastructure.database.models import User

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def create_access_token(data: dict = None) -> str:
    return create_access_token(data)

def create_refresh_token(data: dict = None) -> str:
    return create_refresh_token(data)

def signup_user(db: Session, user: User) -> UserResponse:
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_password(token, SECRET_KEY)
    if not token:
        raise credentials_exception
    return token

def refresh_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise credentials_exception
        access_token = create_access_token(data={"sub": user.username})
        return access_token
    except jwt.exceptions.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e