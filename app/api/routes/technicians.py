from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.dependencies import get_current_admin_user
from app.services import technician_service
from app.schemas.technician import (
    TechnicianCreate,
    TechnicianUpdate,
    TechnicianResponse,
)

router = APIRouter(
    prefix="/technicians",
    tags=["Technicians"],
)


@router.post(
    "",
    response_model=TechnicianResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_technician(
    technician: TechnicianCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return technician_service.create_technician(db, technician)


@router.get("", response_model=list[TechnicianResponse])
def get_technicians(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    department: str | None = Query(None),
    is_active: bool | None = Query(True),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return technician_service.get_all_technicians(
        db, limit, offset, department, is_active
    )


@router.get("/{technician_id}", response_model=TechnicianResponse)
def get_technician(
    technician_id: int = Path(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return technician_service.get_technician_by_id(db, technician_id)


@router.patch("/{technician_id}", response_model=TechnicianResponse)
def update_technician(
    technician_id: int,
    update_data: TechnicianUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    return technician_service.update_technician(db, technician_id, update_data)


@router.delete("/{technician_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technician(
    technician_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    technician_service.delete_technician(db, technician_id)
    return
