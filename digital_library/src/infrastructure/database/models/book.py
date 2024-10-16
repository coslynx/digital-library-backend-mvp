from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from infrastructure.database.models import Base

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