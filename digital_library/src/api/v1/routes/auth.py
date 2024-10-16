from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from infrastructure.database.db_session import get_db
from infrastructure.config import settings
from api.v1.controllers.auth_controller import auth_controller
from api.v1.schemas.auth import Token, User, UserResponse

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth_controller.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_controller.create_access_token(data={"sub": user.username})
    refresh_token = auth_controller.create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@auth_router.post("/refresh_token", response_model=Token)
async def refresh_token(token: str = Depends(auth_controller.get_current_user)):
    refresh_token = auth_controller.refresh_token(token)
    return {"access_token": refresh_token, "refresh_token": refresh_token, "token_type": "bearer"}

@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: User, db: Session = Depends(get_db)):
    return auth_controller.signup_user(db, user)