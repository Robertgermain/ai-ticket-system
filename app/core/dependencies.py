from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import UserModel
from app.core.config import settings

# OAuth2 scheme for extracting Bearer token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Validate JWT token and return the authenticated user.

    This dependency:
    - Decodes and verifies the JWT token
    - Extracts the user ID from the token payload
    - Fetches the user from the database
    - Ensures the account is active

    Raises:
        HTTPException (401): Invalid or missing credentials
        HTTPException (403): User account is inactive
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT and extract payload
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        # Token is invalid, expired, or malformed
        raise credentials_exception

    # Retrieve user from database
    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    # Prevent access for deactivated accounts
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


def get_current_admin_user(
    current_user: UserModel = Depends(get_current_user),
):
    """
    Ensure the current user has admin privileges.

    This dependency builds on get_current_user and enforces
    role-based access control for admin-only operations.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return current_user
