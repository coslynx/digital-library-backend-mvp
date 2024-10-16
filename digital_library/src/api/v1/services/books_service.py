from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.config import settings
from infrastructure.database.db_session import get_db
from api.v1.schemas.book import Book, BookCreate, BookResponse
from infrastructure.database.models import Book

from utils.auth import get_current_user
from api.v1.schemas.auth import User

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