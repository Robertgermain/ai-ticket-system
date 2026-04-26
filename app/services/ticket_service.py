from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketUserUpdate
from app.models.user import UserModel


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
