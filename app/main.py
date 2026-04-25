from fastapi import FastAPI
from app.api.routes import tickets
from app.db.database import engine
from app.models.ticket import TicketModel

TicketModel.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "AI Ticket Processing System is running"}


app.include_router(tickets.router)
