from fastapi import FastAPI
from app.api.routes import tickets

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "AI Ticket Processing System is running"}


app.include_router(tickets.router)
