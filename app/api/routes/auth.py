from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.services import user_service
from app.db.deps import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, password, and profile information.",
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new user if the email is not already in use."""

    # Ensure email uniqueness before creating the account
    existing_user = user_service.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create user with default role 'user'
    return user_service.create_user(
        db,
        user.email,
        user.password,
        role="user",
        first_name=user.first_name,
        last_name=user.last_name,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and return access token",
    description="Validate user credentials and return a JWT access token.",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate user credentials and issue a JWT access token."""

    # OAuth2 uses "username" field for email
    db_user = user_service.get_user_by_email(db, form_data.username)

    # Validate credentials (user exists and password matches)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Block login for inactive accounts
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Generate JWT with user identity and role for downstream authorization
    token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
            "role": db_user.role,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
