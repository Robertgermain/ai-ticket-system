from pydantic import BaseModel


# Base model for creating a new ticket from user input
class TicketCreate(BaseModel):
    title: str
    description: str


# Base model for returning the ticket data once created
class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: str
