from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Empty list to store tickets. (This will be converted to a database later)
tickets = []


# Base model for creating a new ticket from user input
class TicketCreate(BaseModel):
    title: str


# Base model for returning the ticket data once created
class Ticket(BaseModel):
    id: int
    title: str
    status: str


@app.get("/")
async def test():
    return {"message": "AI Ticket Processing System is running"}


@app.get("/tickets", response_model=list[Ticket])
async def get_tickets():
    return tickets


@app.post("/tickets")
async def create_ticket(ticket: TicketCreate, response_model=Ticket):
    # Auto-generates ID and sets default ticket status
    new_ticket = {"id": len(tickets) + 1, "title": ticket.title, "status": "open"}
    tickets.append(new_ticket)
    return new_ticket
