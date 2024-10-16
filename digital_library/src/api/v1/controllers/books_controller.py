from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from api.v1.services.books_service import books_service
from api.v1.schemas.book import Book, BookCreate, BookResponse

# Import the necessary dependencies for the controller
from infrastructure.config import settings
from utils.auth import get_current_user

# Import the necessary dependencies for the controller
from api.v1.schemas.auth import Token, User, UserResponse

# Define the router for the books controller
books_router = APIRouter()

# Define the function to create a new book
@books_router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Creates a new book in the library catalog."""
    # Call the create_book function from the books service
    new_book = await books_service.create_book(db, book)
    return new_book

# Define the function to get all books
@books_router.get("/", response_model=list[BookResponse])
async def get_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves a list of all books in the library catalog."""
    # Call the get_books function from the books service
    books = await books_service.get_books(db)
    return books

# Define the function to get a specific book by ID
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

# Define the function to update a specific book by ID
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

# Define the function to delete a specific book by ID
@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Deletes a specific book from the library catalog."""
    # Call the delete_book function from the books service
    await books_service.delete_book(db, book_id)