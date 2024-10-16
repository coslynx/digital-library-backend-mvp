from pydantic import BaseModel, Field
from datetime import datetime

class Token(BaseModel):
    access_token: str = Field(..., description="The access token for authenticating requests.")
    refresh_token: str = Field(..., description="The refresh token for generating new access tokens.")
    token_type: str = Field("bearer", description="The type of the tokens.")

class User(BaseModel):
    username: str = Field(..., description="The username of the user.")
    password: str = Field(..., description="The password of the user.")

class UserResponse(BaseModel):
    id: int = Field(..., description="The ID of the user.")
    username: str = Field(..., description="The username of the user.")
    created_at: datetime = Field(..., description="The date and time the user was created.")
    updated_at: datetime = Field(..., description="The date and time the user was last updated.")