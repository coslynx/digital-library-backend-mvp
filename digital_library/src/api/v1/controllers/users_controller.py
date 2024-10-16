from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from api.v1.services.users_service import users_service
from api.v1.schemas.user import User, UserCreate, UserResponse

users_router = APIRouter()

@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Creates a new user account in the library system."""
    new_user = await users_service.create_user(db, user)
    return new_user

@users_router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """Retrieves a list of all users in the library system."""
    users = await users_service.get_users(db)
    return users

@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieves details of a specific user by ID."""
    user = await users_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user

@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    """Updates the details of a specific user by ID."""
    updated_user = await users_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return updated_user

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deletes a specific user account by ID."""
    await users_service.delete_user(db, user_id)