from fastapi import APIRouter

from api.v1.routes import users, books, auth

api_router = APIRouter()

api_router.include_router(users.users_router, prefix="/users", tags=["users"])
api_router.include_router(books.books_router, prefix="/books", tags=["books"])
api_router.include_router(auth.auth_router, prefix="/auth", tags=["auth"])