from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.technician import TechnicianModel


def _get_technician(db: Session, technician_id: int):
    """Retrieve a technician by ID."""
    return db.query(TechnicianModel).filter(TechnicianModel.id == technician_id).first()


def create_technician(db: Session, technician_data):
    """Create a new technician."""

    existing = (
        db.query(TechnicianModel)
        .filter(TechnicianModel.email == technician_data.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Technician with this email already exists",
        )

    technician = TechnicianModel(
        first_name=technician_data.first_name,
        last_name=technician_data.last_name,
        email=technician_data.email,
        role_title=technician_data.role_title,
        department=technician_data.department,
        skill_level=technician_data.skill_level,
        skills=technician_data.skills,
        max_ticket_capacity=technician_data.max_ticket_capacity,
    )

    db.add(technician)
    db.commit()
    db.refresh(technician)
    return technician


def get_all_technicians(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    department: str | None = None,
    is_active: bool | None = True,
):
    """Retrieve technicians with optional filtering."""

    query = db.query(TechnicianModel)

    if is_active is not None:
        query = query.filter(TechnicianModel.is_active == is_active)

    if department:
        query = query.filter(TechnicianModel.department == department)

    return (
        query.order_by(TechnicianModel.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_technician_by_id(db: Session, technician_id: int):
    """Retrieve a technician by ID."""

    technician = _get_technician(db, technician_id)

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician not found",
        )

    return technician


def update_technician(db: Session, technician_id: int, update_data):
    """Update technician details."""

    technician = _get_technician(db, technician_id)

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician not found",
        )

    update_fields = update_data.model_dump(exclude_unset=True)

    for key, value in update_fields.items():
        setattr(technician, key, value)

    db.commit()
    db.refresh(technician)
    return technician


def delete_technician(db: Session, technician_id: int):
    """Soft delete technician (set inactive)."""

    technician = _get_technician(db, technician_id)

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician not found",
        )

    technician.is_active = False

    db.commit()
    db.refresh(technician)
    return technician
