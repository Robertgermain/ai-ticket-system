from fastapi import FastAPI
import logging

from app.api.routes import tickets, auth, users
from app.db.database import engine, Base
from app.models import ticket, user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="AI Ticket Processing System",
    description="Backend system for AI-powered ticket classification and processing",
    version="1.0.0",
)


@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "AI Ticket Processing System is running"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tickets.router)
