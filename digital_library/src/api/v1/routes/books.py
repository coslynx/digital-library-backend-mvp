from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from api.v1.controllers.books_controller import books_controller
from api.v1.schemas.book import Book, BookCreate, BookResponse

books_router = APIRouter()

@books_router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return books_controller.create_book(db, book)

@books_router.get("/", response_model=list[BookResponse])
async def get_books(db: Session = Depends(get_db)):
    return books_controller.get_books(db)

@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = books_controller.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return book

@books_router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    return books_controller.update_book(db, book_id, book)

@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    books_controller.delete_book(db, book_id)