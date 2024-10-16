from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookBase(BaseModel):
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    isbn: str = Field(..., description="ISBN number of the book")
    genre: str = Field(..., description="Genre of the book")
    description: Optional[str] = Field(None, description="Description of the book")
    publication_date: date = Field(..., description="Publication date of the book")
    cover_image: Optional[str] = Field(None, description="URL to the cover image of the book")

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int = Field(..., description="ID of the book")
    is_available: bool = Field(..., description="Indicates whether the book is currently available for borrowing")
    borrower_id: Optional[int] = Field(None, description="ID of the user who has borrowed the book, if any")

class BookUpdate(BookBase):
    is_available: Optional[bool] = Field(None, description="Whether the book is available for borrowing (can be used to change the availability status)")
    borrower_id: Optional[int] = Field(None, description="ID of the user who has borrowed the book (can be used to change the borrower)")