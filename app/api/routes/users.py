from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.dependencies import get_current_user
from app.services import user_service
from app.models.user import User
from app.schemas.user import AdminUserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(User).all()


@router.patch("/{user_id}/role")
def update_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_user_role(db, user_id, new_role, current_user)


@router.post("/")
def create_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.create_user(db, user.email, user.password, user.role)
