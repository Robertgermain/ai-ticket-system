from fastapi import FastAPI
from app.api.routes import tickets
from app.db.database import engine, Base
from app.models import ticket, user
from app.api.routes import auth
from app.api.routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "AI Ticket Processing System is running"}


app.include_router(tickets.router)
app.include_router(auth.router)
app.include_router(users.router)
