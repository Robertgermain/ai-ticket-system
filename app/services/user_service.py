from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import UserModel
from app.core.security import hash_password


def _get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def _check_admin(user: UserModel):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )


def _check_self_or_admin(current_user: UserModel, target_user_id: int):
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
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_all_users(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    role: str | None = None,
    is_active: bool | None = True,
):
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
