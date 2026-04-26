from app.db.database import SessionLocal


def get_db():
    """
    Provide a database session for request handling.

    This dependency:
    - Creates a new SQLAlchemy session per request
    - Yields the session to the route/service layer
    - Ensures the session is properly closed after the request completes
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
