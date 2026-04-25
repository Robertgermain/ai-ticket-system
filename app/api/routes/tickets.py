from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.ticket import TicketCreate, Ticket, TicketUpdate
from app.services import ticket_service
from app.db.deps import get_db
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[Ticket])
async def get_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ticket_service.get_tickets(db, current_user)


@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ticket = ticket_service.get_ticket_by_id(db, ticket_id, current_user)

    if ticket == "unauthorized":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.post(
    "",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ticket_service.create_ticket(db, ticket, current_user)


@router.put("/{ticket_id}", response_model=Ticket)
async def update_ticket(
    ticket_id: int,
    updated_ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ticket = ticket_service.update_ticket(db, ticket_id, updated_ticket, current_user)

    if ticket == "unauthorized":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = ticket_service.delete_ticket(db, ticket_id, current_user)

    if result == "unauthorized":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return
