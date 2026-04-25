from sqlalchemy.orm import Session
from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate


def get_tickets(db: Session):
    return db.query(TicketModel).order_by(TicketModel.id).all()


def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(TicketModel).filter(TicketModel.id == ticket_id).first()


def create_ticket(db: Session, ticket: TicketCreate):
    new_ticket = TicketModel(
        title=ticket.title,
        description=ticket.description,
        status="open",
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


def update_ticket(db: Session, ticket_id: int, updated_ticket: TicketCreate):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()

    if not ticket:
        return None

    ticket.title = updated_ticket.title
    ticket.description = updated_ticket.description

    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()

    if not ticket:
        return None

    db.delete(ticket)
    db.commit()
    return ticket
