from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.core.security import hash_password


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
        return None

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


def get_all_users(db: Session):
    return db.query(UserModel).filter(UserModel.is_active == True).all()


def update_user_role(
    db: Session, target_user_id: int, new_role: str, current_user: UserModel
):
    if current_user.role != "admin":
        return "unauthorized"

    if current_user.id == target_user_id:
        return "unauthorized"

    user = db.query(UserModel).filter(UserModel.id == target_user_id).first()
    if not user:
        return None

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, target_user_id: int, user_update, current_user: UserModel):
    if current_user.role != "admin" and current_user.id != target_user_id:
        return "unauthorized"

    user = db.query(UserModel).filter(UserModel.id == target_user_id).first()
    if not user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, target_user_id: int, current_user: UserModel):
    if current_user.role != "admin":
        return "unauthorized"

    if current_user.id == target_user_id:
        return "unauthorized"

    user = db.query(UserModel).filter(UserModel.id == target_user_id).first()
    if not user:
        return None

    user.is_active = False

    db.commit()
    db.refresh(user)
    return user
