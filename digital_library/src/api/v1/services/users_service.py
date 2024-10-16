from fastapi import HTTPException, status
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