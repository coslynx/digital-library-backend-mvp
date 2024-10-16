from infrastructure.database.db_session import get_db
from infrastructure.database.models import User, Book
from infrastructure.config import settings
from sqlalchemy.orm import Session

# Import dummy data or read data from a file, ensuring consistent data format
from scripts.dummy_data import users, books

def seed_users(db: Session):
    for user_data in users:
        db_user = User(**user_data)
        db.add(db_user)
    db.commit()

def seed_books(db: Session):
    for book_data in books:
        db_book = Book(**book_data)
        db.add(db_book)
    db.commit()

if __name__ == "__main__":
    with get_db() as db:
        seed_users(db)
        seed_books(db)