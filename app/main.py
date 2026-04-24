from fastapi import FastAPI

app = FastAPI()

tickets = []


@app.get("/")
async def test():
    return {"message": "AI Ticket Processing System is running"}


@app.get("/tickets")
async def get_tickets():
    return tickets


@app.post("/tickets")
async def create_ticket():
    ticket = {"id": len(tickets) + 1, "title": "Sample Ticket", "status": "open"}
    tickets.append(ticket)
    return ticket
