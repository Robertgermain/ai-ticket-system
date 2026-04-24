from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def test():
    return {"message": "AI Ticket Processing System is running"}
