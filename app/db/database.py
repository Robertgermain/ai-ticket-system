import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

# Load environment variables
load_dotenv()

# Use a single source of truth for DB connection
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine (handles DB connections)
engine = create_engine(DATABASE_URL)

# Session factory for DB operations
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for all ORM models
Base = declarative_base()


# FastAPI DB Dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
