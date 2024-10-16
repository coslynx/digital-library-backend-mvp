from typing import Union, Type, Any

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from infrastructure.config import settings
from utils.response_handler import create_error_response


class BaseException(Exception):
    """Base exception class for all custom exceptions in the application."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: Union[str, dict] = None) -> None:
        """
        Initializes the BaseException with a message, status code, and optional details.

        Args:
            message: The error message to be displayed.
            status_code: The HTTP status code for the error.
            details: Optional additional details about the error.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class AuthenticationError(BaseException):
    """Custom exception for authentication failures."""

    def __init__(self, message: str = "Authentication failed. Please check your credentials.", details: Union[str, dict] = None) -> None:
        """
        Initializes the AuthenticationError with a message and optional details.

        Args:
            message: The error message to be displayed.
            details: Optional additional details about the error.
        """
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, details=details)


class NotFoundError(BaseException):
    """Custom exception for resources that are not found."""

    def __init__(self, message: str = "Resource not found.", details: Union[str, dict] = None) -> None:
        """
        Initializes the NotFoundError with a message and optional details.

        Args:
            message: The error message to be displayed.
            details: Optional additional details about the error.
        """
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, details=details)


class BadRequestError(BaseException):
    """Custom exception for invalid or malformed requests."""

    def __init__(self, message: str = "Invalid request.", details: Union[str, dict] = None) -> None:
        """
        Initializes the BadRequestError with a message and optional details.

        Args:
            message: The error message to be displayed.
            details: Optional additional details about the error.
        """
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST, details=details)


class DatabaseError(BaseException):
    """Custom exception for database-related errors."""

    def __init__(self, message: str = "Database error occurred.", details: Union[str, dict] = None) -> None:
        """
        Initializes the DatabaseError with a message and optional details.

        Args:
            message: The error message to be displayed.
            details: Optional additional details about the error.
        """
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=details)


class InternalServerError(BaseException):
    """Custom exception for internal server errors."""

    def __init__(self, message: str = "An unexpected error occurred.", details: Union[str, dict] = None) -> None:
        """
        Initializes the InternalServerError with a message and optional details.

        Args:
            message: The error message to be displayed.
            details: Optional additional details about the error.
        """
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=details)


def handle_exception(exc: Exception) -> JSONResponse:
    """
    Handles exceptions and returns a standardized JSON response.

    Args:
        exc: The caught exception.

    Returns:
        JSONResponse: A JSON response with an error message and details.
    """
    if isinstance(exc, BaseException):
        return create_error_response(message=exc.message, status_code=exc.status_code, details=exc.details)
    else:
        return create_error_response(message="An unexpected error occurred.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=str(exc))