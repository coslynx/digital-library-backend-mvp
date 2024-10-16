from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

from api.v1.schemas.user import UserBase
from api.v1.schemas.book import BookBase

class Token(BaseModel):
    access_token: str = Field(..., description="The access token for authenticating requests.")
    refresh_token: str = Field(..., description="The refresh token for generating new access tokens.")
    token_type: str = Field("bearer", description="The type of the tokens.")

class User(BaseModel):
    username: str = Field(..., description="The username of the user.")
    password: str = Field(..., description="The password of the user.")

class UserResponse(UserBase):
    id: int = Field(..., description="The ID of the user.")
    created_at: datetime = Field(..., description="The date and time the user was created.")
    updated_at: datetime = Field(..., description="The date and time the user was last updated.")

class Book(BaseModel):
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