from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.ticket import TicketCreate, Ticket
from app.services import ticket_service
from app.db.deps import get_db

router = APIRouter()


@router.get("/tickets", response_model=list[Ticket])
async def get_tickets(db: Session = Depends(get_db)):
    return ticket_service.get_tickets(db)


@router.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    ticket = ticket_service.get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket


@router.post(
    "/tickets",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    return ticket_service.create_ticket(db, ticket)


@router.put("/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket(
    ticket_id: int,
    updated_ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    ticket = ticket_service.update_ticket(db, ticket_id, updated_ticket)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket


@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    ticket = ticket_service.delete_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return
