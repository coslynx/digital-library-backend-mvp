from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from api.v1.controllers.users_controller import users_controller
from api.v1.schemas.user import User, UserCreate, UserResponse

users_router = APIRouter()

@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return users_controller.create_user(db, user)

@users_router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return users_controller.get_users(db)

@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = users_controller.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user

@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    return users_controller.update_user(db, user_id, user)

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    users_controller.delete_user(db, user_id)