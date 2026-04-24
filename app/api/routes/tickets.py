from fastapi import APIRouter, HTTPException, status
from app.schemas.ticket import TicketCreate, Ticket

router = APIRouter()

# Simple ID counter to ensure unique ticket IDs (temporary until DB is added)
ticket_id_counter = 1

# In-memory storage for tickets (temporary; will be replaced with a database)
tickets = []


@router.get("/tickets", response_model=list[Ticket])
async def get_tickets():
    # Return all tickets
    return tickets


@router.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(ticket_id: int):
    # Find ticket by ID (returns None if not found)
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        # Return 404 if ticket does not exist
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
    global ticket_id_counter

    # Auto-generate ID and set default status
    new_ticket = {
        "id": ticket_id_counter,
        "title": ticket.title,
        "description": ticket.description,
        "status": "open",
    }
    tickets.append(new_ticket)
    ticket_id_counter += 1
    return new_ticket


@router.put("/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket(ticket_id: int, updated_ticket: TicketCreate):
    # Find existing ticket
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    # Update ticket fields
    ticket["title"] = updated_ticket.title
    ticket["description"] = updated_ticket.description
    return ticket


@router.delete("/tickets/{ticket_id}", response_model=Ticket)
async def delete_ticket(ticket_id: int):
    # Locate ticket to delete
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    # Remove ticket from storage
    tickets.remove(ticket)
    return ticket
