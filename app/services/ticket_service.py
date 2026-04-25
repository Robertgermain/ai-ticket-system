from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate
from app.models.user import User


def get_tickets(db: Session, user: User):
    if user.role == "admin":
        return db.query(TicketModel).order_by(TicketModel.id).all()
    return (
        db.query(TicketModel)
        .filter(TicketModel.owner_id == user.id)
        .order_by(TicketModel.id)
        .all()
    )


def get_ticket_by_id(db: Session, ticket_id: int, user: User):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    if user.role != "admin" and ticket.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this ticket",
        )
    return ticket


def create_ticket(db: Session, ticket: TicketCreate, user: User):
    new_ticket = TicketModel(
        title=ticket.title,
        description=ticket.description,
        status="open",
        owner_id=user.id,  # ✅ FIXED
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


def update_ticket(
    db: Session,
    ticket_id: int,
    updated_ticket: TicketCreate,
    user: User,
):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    if user.role != "admin" and ticket.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this ticket",
        )
    ticket.title = updated_ticket.title
    ticket.description = updated_ticket.description

    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int, user: User):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete tickets",
        )
    db.delete(ticket)
    db.commit()
    return
