from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return user_service.get_all_users(db)


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    user = user_service.update_user_role(db, user_id, role_update.role, current_user)

    if user == "unauthorized":
        raise HTTPException(status_code=403, detail="Not authorized")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    user = user_service.update_user(db, user_id, user_update, current_user)

    if user == "unauthorized":
        raise HTTPException(status_code=403, detail="Not authorized")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    result = user_service.delete_user(db, user_id, current_user)

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not authorized")

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
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
