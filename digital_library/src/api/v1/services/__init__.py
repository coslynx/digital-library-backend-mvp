from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.config import settings
from infrastructure.database.db_session import get_db
from api.v1.schemas.user import User, UserCreate, UserResponse
from infrastructure.database.models import User

from utils.auth import get_current_user
from api.v1.schemas.auth import User

async def create_user(db: Session, user: UserCreate, current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Creates a new user account in the library system.
    """
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)

async def get_users(db: Session, current_user: User = Depends(get_current_user)) -> list[UserResponse]:
    """
    Retrieves a list of all users in the library system.
    """
    users = db.query(User).all()
    return [UserResponse.from_orm(user) for user in users]

async def get_user(db: Session, user_id: int, current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Retrieves details of a specific user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return UserResponse.from_orm(user)

async def update_user(db: Session, user_id: int, user: User, current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Updates the details of a specific user by ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)

async def delete_user(db: Session, user_id: int, current_user: User = Depends(get_current_user)):
    """
    Deletes a specific user account by ID.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    db.delete(db_user)
    db.commit()

async def create_book(db: Session, book: BookCreate, current_user: User = Depends(get_current_user)) -> BookResponse:
    """
    Creates a new book in the library catalog.
    """
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookResponse.from_orm(db_book)

async def get_books(db: Session, current_user: User = Depends(get_current_user)) -> list[BookResponse]:
    """
    Retrieves a list of all books in the library catalog.
    """
    books = db.query(Book).all()
    return [BookResponse.from_orm(book) for book in books]

async def get_book(db: Session, book_id: int, current_user: User = Depends(get_current_user)) -> BookResponse:
    """
    Retrieves details of a specific book by its ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return BookResponse.from_orm(book)

async def update_book(db: Session, book_id: int, book: Book, current_user: User = Depends(get_current_user)) -> BookResponse:
    """
    Updates the details of a specific book by its ID.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    update_data = book.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return BookResponse.from_orm(db_book)

async def delete_book(db: Session, book_id: int, current_user: User = Depends(get_current_user)):
    """
    Deletes a specific book from the library catalog.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    db.delete(db_book)
    db.commit()

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
        access_token = create_access_token(data={\"sub\": user.username})
        return access_token
    except jwt.exceptions.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e