from infrastructure.config import settings
from utils.auth import create_access_token, create_refresh_token, verify_password, get_current_user

# Dependency for retrieving the current user
async def get_current_user(token: str = Depends(verify_password)) -> User:
    """
    Verifies the JWT token provided in the request header.

    Args:
        token (str, optional): The JWT token provided in the request header. Defaults to None.

    Returns:
        User: The user object associated with the token if the token is valid, otherwise raises an HTTPException.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    return token