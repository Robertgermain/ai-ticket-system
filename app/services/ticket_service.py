from sqlalchemy.orm import Session

from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.user import UserModel


def get_tickets(db: Session, user: UserModel):
    query = db.query(TicketModel).filter(TicketModel.is_deleted == False)

    if user.role != "admin":
        query = query.filter(TicketModel.owner_id == user.id)

    return query.order_by(TicketModel.id).all()


def get_ticket_by_id(db: Session, ticket_id: int, user: UserModel):
    ticket = (
        db.query(TicketModel)
        .filter(
            TicketModel.id == ticket_id,
            TicketModel.is_deleted == False,
        )
        .first()
    )

    if not ticket:
        return None

    if user.role != "admin" and ticket.owner_id != user.id:
        return "unauthorized"

    return ticket


def create_ticket(db: Session, ticket: TicketCreate, user: UserModel):
    new_ticket = TicketModel(
        **ticket.model_dump(),
        owner_id=user.id,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


def update_ticket(
    db: Session,
    ticket_id: int,
    updated_ticket: TicketUpdate,
    user: UserModel,
):
    ticket = (
        db.query(TicketModel)
        .filter(
            TicketModel.id == ticket_id,
            TicketModel.is_deleted == False,
        )
        .first()
    )

    if not ticket:
        return None

    if user.role != "admin" and ticket.owner_id != user.id:
        return "unauthorized"

    update_data = updated_ticket.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int, user: UserModel):
    ticket = (
        db.query(TicketModel)
        .filter(
            TicketModel.id == ticket_id,
            TicketModel.is_deleted == False,
        )
        .first()
    )

    if not ticket:
        return None

    if user.role != "admin" and ticket.owner_id != user.id:
        return "unauthorized"

    ticket.is_deleted = True

    db.commit()
    db.refresh(ticket)
    return ticket
