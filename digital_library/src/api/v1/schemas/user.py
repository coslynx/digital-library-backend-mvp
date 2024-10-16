from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., description="The username of the user.")
    email: str = Field(..., description="The email address of the user.")
    password: str = Field(..., description="The password of the user.")

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int = Field(..., description="The ID of the user.")
    created_at: datetime = Field(..., description="The date and time the user was created.")
    updated_at: datetime = Field(..., description="The date and time the user was last updated.")