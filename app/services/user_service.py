from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import UserModel
from app.core.security import hash_password


def _get_user(db: Session, user_id: int):
    """Retrieve a user by ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def _check_admin(user: UserModel):
    """Ensure the current user has admin privileges."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )


def _check_self_or_admin(current_user: UserModel, target_user_id: int):
    """
    Ensure the user is either:
    - Acting on their own account, OR
    - Has admin privileges
    """
    if current_user.role != "admin" and current_user.id != target_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )


def create_user(
    db: Session,
    email: str,
    password: str,
    role: str = "user",
    first_name: str = "",
    last_name: str = "",
):
    """
    Create a new user account.

    - Ensures email uniqueness
    - Hashes password before storing
    - Defaults to active user
    """

    existing = db.query(UserModel).filter(UserModel.email == email).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = UserModel(
        email=email,
        hashed_password=hash_password(password),
        role=role,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    """Retrieve a user by email (used for authentication)."""
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_all_users(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    role: str | None = None,
    is_active: bool | None = True,
):
    """
    Retrieve users with optional filtering and pagination.

    Filters:
    - role (admin/user)
    - active status
    """

    query = db.query(UserModel)

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    if role:
        query = query.filter(UserModel.role == role)

    return query.order_by(UserModel.created_at.desc()).limit(limit).offset(offset).all()


def get_user_by_id(
    db: Session,
    user_id: int,
    current_user: UserModel,
):
    """
    Retrieve a user by ID with access control.

    Users can:
    - View their own profile
    - Admins can view any user
    """

    user = _get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    _check_self_or_admin(current_user, user_id)

    return user


def update_user_role(
    db: Session,
    target_user_id: int,
    new_role: str,
    current_user: UserModel,
):
    """
    Update a user's role (admin only).

    Restrictions:
    - Admins cannot modify their own role
    """

    _check_admin(current_user)

    if current_user.id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify your own role",
        )

    user = _get_user(db, target_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.role = new_role

    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session,
    target_user_id: int,
    user_update,
    current_user: UserModel,
):
    """
    Update user profile fields.

    - Users can update their own profile
    - Admins can update any user
    - Restricted fields are enforced at schema level
    """

    _check_self_or_admin(current_user, target_user_id)

    user = _get_user(db, target_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(
    db: Session,
    target_user_id: int,
    current_user: UserModel,
):
    """
    Soft delete a user (admin only).

    - Marks user as inactive instead of deleting from DB
    - Prevents self-deletion
    """

    _check_admin(current_user)

    if current_user.id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    user = _get_user(db, target_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_active = False

    db.commit()
    db.refresh(user)
    return user
