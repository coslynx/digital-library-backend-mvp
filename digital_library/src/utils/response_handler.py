from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Union, Dict, Any
from infrastructure.config import settings


def create_success_response(data: Union[Dict[str, Any], List[Dict[str, Any]]], message: str = None) -> JSONResponse:
    """
    Creates a success response for API endpoints.

    Args:
        data: The data to be included in the response.
        message: An optional success message.

    Returns:
        JSONResponse: A JSON response with status code 200 and the provided data and message.
    """
    response_data = {"data": data}
    if message:
        response_data["message"] = message
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)


def create_error_response(message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: str = None) -> JSONResponse:
    """
    Creates an error response for API endpoints.

    Args:
        message: The error message to be included in the response.
        status_code: The HTTP status code for the error.
        details: Optional additional details about the error.

    Returns:
        JSONResponse: A JSON response with the specified status code and the provided error message and details.
    """
    response_data = {"message": message}
    if details:
        response_data["details"] = details
    return JSONResponse(status_code=status_code, content=response_data)


def handle_database_error(exc: Exception) -> JSONResponse:
    """
    Handles database-related errors and returns a standardized error response.

    Args:
        exc: The caught database error.

    Returns:
        JSONResponse: A JSON response with status code 500 and a database error message.
    """
    return create_error_response(
        message="Database error occurred. Please try again later.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=str(exc),
    )


def handle_authentication_error(exc: Exception) -> JSONResponse:
    """
    Handles authentication-related errors and returns a standardized error response.

    Args:
        exc: The caught authentication error.

    Returns:
        JSONResponse: A JSON response with status code 401 and an authentication error message.
    """
    return create_error_response(
        message="Authentication failed. Please check your credentials.",
        status_code=status.HTTP_401_UNAUTHORIZED,
        details=str(exc),
    )


def handle_validation_error(exc: Exception) -> JSONResponse:
    """
    Handles validation errors and returns a standardized error response.

    Args:
        exc: The caught validation error.

    Returns:
        JSONResponse: A JSON response with status code 400 and a validation error message.
    """
    return create_error_response(
        message="Invalid data provided. Please check your input.",
        status_code=status.HTTP_400_BAD_REQUEST,
        details=str(exc),
    )


def handle_generic_error(exc: Exception) -> JSONResponse:
    """
    Handles generic errors and returns a standardized error response.

    Args:
        exc: The caught generic error.

    Returns:
        JSONResponse: A JSON response with status code 500 and a generic error message.
    """
    if settings.DEBUG:
        return create_error_response(
            message="An unexpected error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(exc),
        )
    else:
        return create_error_response(
            message="An unexpected error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )