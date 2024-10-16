from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    borrowed_books = relationship("Book", backref="borrower", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)
    genre = Column(String, nullable=False)
    description = Column(String, nullable=True)
    publication_date = Column(Date, nullable=False)
    cover_image = Column(String, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    borrower = relationship("User", backref="borrowed_books")