from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketUserUpdate
from app.models.user import UserModel
from app.services.ai_service import analyze_ticket

logger = logging.getLogger(__name__)


def _get_ticket(db: Session, ticket_id: int):
    return (
        db.query(TicketModel)
        .filter(
            TicketModel.id == ticket_id,
            TicketModel.is_deleted == False,
        )
        .first()
    )


def _check_ticket_access(ticket: TicketModel, user: UserModel):
    if user.role != "admin" and ticket.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )


def _sanitize_ai_output(ai_data: dict) -> dict:
    """Ensure AI output is safe and valid before writing to DB"""

    allowed_priorities = {"low", "medium", "high"}
    allowed_status = {"open", "in_progress", "closed"}
    allowed_ticket_types = {"incident", "request", "alert"}
    allowed_categories = {
        "hardware",
        "software",
        "network",
        "security",
        "access",
        "other",
    }

    sanitized = {
        "summary": ai_data.get("summary"),
        "priority": (
            ai_data.get("priority")
            if ai_data.get("priority") in allowed_priorities
            else "medium"
        ),
        "status": (
            ai_data.get("status") if ai_data.get("status") in allowed_status else "open"
        ),
        "category": (
            ai_data.get("category")
            if ai_data.get("category") in allowed_categories
            else "other"
        ),
        "issue_type": ai_data.get("issue_type"),
        "sub_issue_type": ai_data.get("sub_issue_type"),
        "ticket_type": (
            ai_data.get("ticket_type")
            if ai_data.get("ticket_type") in allowed_ticket_types
            else "incident"
        ),
    }

    return sanitized


def get_tickets(
    db: Session,
    user: UserModel,
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    priority: str | None = None,
):
    query = db.query(TicketModel).filter(TicketModel.is_deleted == False)

    if user.role != "admin":
        query = query.filter(TicketModel.owner_id == user.id)

    if status:
        query = query.filter(TicketModel.status == status)

    if priority:
        query = query.filter(TicketModel.priority == priority)

    return (
        query.order_by(TicketModel.created_at.desc()).limit(limit).offset(offset).all()
    )


def get_ticket_by_id(db: Session, ticket_id: int, user: UserModel):
    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    _check_ticket_access(ticket, user)
    return ticket


def create_ticket(db: Session, ticket: TicketCreate, user: UserModel):
    new_ticket = TicketModel(
        title=ticket.title,
        description=ticket.description,
        owner_id=user.id,
    )

    try:
        ai_data = analyze_ticket(ticket.title, ticket.description)

        logger.info("AI RAW OUTPUT: %s", ai_data)

        ai_data = _sanitize_ai_output(ai_data)

        logger.info("AI SANITIZED OUTPUT: %s", ai_data)

        for key, value in ai_data.items():
            setattr(new_ticket, key, value)

    except Exception as e:
        logger.error("AI ERROR: %s", e)

        # Safe fallback defaults
        new_ticket.priority = "medium"
        new_ticket.status = "open"
        new_ticket.category = "other"
        new_ticket.ticket_type = "incident"

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


def update_ticket_user(
    db: Session,
    ticket_id: int,
    updated_ticket: TicketUserUpdate,
    user: UserModel,
):
    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    _check_ticket_access(ticket, user)

    update_data = updated_ticket.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket


def update_ticket(
    db: Session,
    ticket_id: int,
    updated_ticket: TicketUpdate,
    user: UserModel,
):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    update_data = updated_ticket.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int, user: UserModel):
    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    _check_ticket_access(ticket, user)

    ticket.is_deleted = True

    db.commit()
    db.refresh(ticket)
    return ticket
