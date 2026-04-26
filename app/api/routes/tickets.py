from fastapi import APIRouter, Depends, status, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.schemas.ticket import (
    TicketCreate,
    Ticket,
    TicketUpdate,
    TicketUserUpdate,
)
from app.services import ticket_service
from app.db.deps import get_db
from app.core.dependencies import get_current_user
from app.models.user import UserModel


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.get("", response_model=list[Ticket])
async def get_tickets(
    limit: int = Query(50, le=100, description="Number of tickets to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    status: str | None = Query(
        None, description="Filter tickets by status (open, in_progress, closed)"
    ),
    priority: str | None = Query(
        None, description="Filter tickets by priority (low, medium, high)"
    ),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve tickets with optional filtering and pagination."""
    return ticket_service.get_tickets(db, current_user, limit, offset, status, priority)


@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(
    ticket_id: int = Path(..., description="ID of the ticket to retrieve"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve a single ticket by ID with access control enforced."""
    return ticket_service.get_ticket_by_id(db, ticket_id, current_user)


@router.post(
    "",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new ticket. AI enrichment is handled in the service layer."""
    return ticket_service.create_ticket(db, ticket, current_user)


@router.patch(
    "/{ticket_id}",
    response_model=Ticket,
    summary="User: Update ticket content",
    description="Allows users to update only the title and description of their ticket.",
)
async def update_ticket_user(
    ticket_id: int = Path(..., description="ID of the ticket to update"),
    updated_ticket: TicketUserUpdate = ...,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Partially update a ticket (user-level).

    Users are restricted to modifying only their own ticket's
    title and description.
    """
    return ticket_service.update_ticket_user(
        db, ticket_id, updated_ticket, current_user
    )


@router.put(
    "/{ticket_id}",
    response_model=Ticket,
    summary="Admin: Fully update ticket",
    description="Allows admins to fully modify all ticket fields including status, priority, and classification.",
)
async def update_ticket_admin(
    ticket_id: int = Path(..., description="ID of the ticket to update"),
    updated_ticket: TicketUpdate = ...,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Fully update a ticket (admin-level).

    Admins can modify all fields including status, priority,
    categorization, and ticket type.
    """

    # Enforce admin-only access at the route layer for clarity and defense-in-depth
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return ticket_service.update_ticket(db, ticket_id, updated_ticket, current_user)


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ticket(
    ticket_id: int = Path(..., description="ID of the ticket to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Soft delete a ticket. Ownership or admin privileges are enforced in the service layer."""
    ticket_service.delete_ticket(db, ticket_id, current_user)
    return
