from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from fastapi import HTTPException, status


def create_user(db: Session, email: str, password: str, role: str = "user"):
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user_role(
    db: Session, target_user_id: int, new_role: str, current_user: User
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change user roles",
        )
    user = db.query(User).filter(User.id == target_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user
