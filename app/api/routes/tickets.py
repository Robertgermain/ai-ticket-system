from fastapi import APIRouter, HTTPException, status
from app.schemas.ticket import TicketCreate, Ticket
from app.services import ticket_service

router = APIRouter()


@router.get("/tickets", response_model=list[Ticket])
async def get_tickets():
    return ticket_service.get_all_tickets()


@router.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(ticket_id: int):
    ticket = ticket_service.get_ticket_by_id(ticket_id)
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
async def create_ticket(ticket: TicketCreate):
    return ticket_service.create_ticket(ticket.title, ticket.description)


@router.put("/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: int, updated_ticket: TicketCreate):
    ticket = ticket_service.update_ticket(
        ticket_id,
        updated_ticket.title,
        updated_ticket.description,
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket


@router.delete("/tickets/{ticket_id}", response_model=Ticket)
async def delete_ticket(ticket_id: int):
    ticket = ticket_service.delete_ticket(ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket
