from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, Literal

from app.db.deps import get_db
from app.core.dependencies import get_current_user
from app.services import user_service
from app.models.user import UserModel
from app.schemas.user import (
    AdminUserCreate,
    UserResponse,
    UserUpdate,
    UserRoleUpdate,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    limit: int = Query(50, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    role: Optional[Literal["admin", "user"]] = Query(
        None, description="Filter by role"
    ),
    is_active: Optional[bool] = Query(
        None, description="Filter by active/inactive users"
    ),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve all users (admin-only) with optional filtering and pagination."""

    # Enforce admin-only access
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return user_service.get_all_users(
        db,
        limit=limit,
        offset=offset,
        role=role,
        is_active=is_active,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's profile information.",
)
def get_current_user_profile(
    current_user: UserModel = Depends(get_current_user),
):
    """Return the currently authenticated user's profile."""
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Allows the authenticated user to update their own first and last name.",
)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update the current user's profile.

    Users are limited to updating their own non-sensitive fields
    (e.g., first name and last name).
    """
    return user_service.update_user(
        db,
        current_user.id,
        user_update,
        current_user,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int = Path(..., description="ID of the user to retrieve"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve a user by ID with access control enforced."""
    return user_service.get_user_by_id(db, user_id, current_user)


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(
    user_id: int = Path(..., description="ID of the user whose role will be updated"),
    role_update: UserRoleUpdate = ...,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update a user's role (admin-only).

    Role changes are restricted to admins and cannot be self-applied.
    """
    return user_service.update_user_role(
        db,
        user_id,
        role_update.role,
        current_user,
    )


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int = Path(..., description="ID of the user to update"),
    user_update: UserUpdate = ...,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update a user (self or admin).

    - Users can update their own profile
    - Admins can update any user
    - Sensitive fields (e.g., role) are handled separately
    """
    return user_service.update_user(
        db,
        user_id,
        user_update,
        current_user,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(..., description="ID of the user to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Deactivate (soft delete) a user account. Admin privileges required."""
    user_service.delete_user(db, user_id, current_user)
    return


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new user (admin-only)."""

    # Enforce admin-only creation
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return user_service.create_user(
        db,
        user.email,
        user.password,
        user.role,
        user.first_name,
        user.last_name,
    )
