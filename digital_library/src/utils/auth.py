from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from infrastructure.config import settings
from infrastructure.database.db_session import get_db
from utils.auth import create_access_token, create_refresh_token, verify_password
from api.v1.schemas.auth import Token, User, UserResponse
from infrastructure.database.models import User

from utils.exceptions import AuthenticationError

# Dependency for retrieving the current user
async def get_current_user(token: str = Depends(verify_password)) -> User:
    """
    Verifies the JWT token provided in the request header.

    Args:
        token (str, optional): The JWT token provided in the request header. Defaults to None.

    Returns:
        User: The user object associated with the token if the token is valid, otherwise raises an HTTPException.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    return token

# Authentication route
@books_router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Creates a new book in the library catalog."""
    # Call the create_book function from the books service
    new_book = await books_service.create_book(db, book)
    return new_book

# Authentication route
@books_router.get("/", response_model=list[BookResponse])
async def get_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves a list of all books in the library catalog."""
    # Call the get_books function from the books service
    books = await books_service.get_books(db)
    return books

# Authentication route
@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves details for a specific book by its ID."""
    # Call the get_book function from the books service
    book = await books_service.get_book(db, book_id)
    # If the book is not found, raise a 404 Not Found exception
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return book

# Authentication route
@books_router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book: Book, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Updates the details of a specific book by its ID."""
    # Call the update_book function from the books service
    updated_book = await books_service.update_book(db, book_id, book)
    # If the book is not found, raise a 404 Not Found exception
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return updated_book

# Authentication route
@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Deletes a specific book from the library catalog."""
    # Call the delete_book function from the books service
    await books_service.delete_book(db, book_id)