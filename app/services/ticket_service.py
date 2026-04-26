from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketUserUpdate
from app.models.user import UserModel
from app.services.ai_service import analyze_ticket

logger = logging.getLogger(__name__)


def _get_ticket(db: Session, ticket_id: int):
    """Retrieve a non-deleted ticket by ID."""
    return (
        db.query(TicketModel)
        .filter(
            TicketModel.id == ticket_id,
            TicketModel.is_deleted == False,
        )
        .first()
    )


def _check_ticket_access(ticket: TicketModel, user: UserModel):
    """Ensure user has access to the ticket (owner or admin)."""
    if user.role != "admin" and ticket.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )


def _sanitize_ai_output(ai_data: dict) -> dict:
    """
    Validate and normalize AI-generated ticket metadata.

    Ensures only allowed values are persisted and applies safe defaults
    when the AI output is invalid or missing fields.
    """

    allowed_priorities = {"low", "medium", "high"}
    allowed_status = {"open", "in_progress", "closed"}
    allowed_ticket_types = {"incident", "request", "alert"}
    allowed_categories = {
        "hardware",
        "software",
        "network",
        "security",
        "access",
        "other",
    }

    return {
        "summary": ai_data.get("summary"),
        "priority": (
            ai_data.get("priority")
            if ai_data.get("priority") in allowed_priorities
            else "medium"
        ),
        "status": (
            ai_data.get("status") if ai_data.get("status") in allowed_status else "open"
        ),
        "category": (
            ai_data.get("category")
            if ai_data.get("category") in allowed_categories
            else "other"
        ),
        "issue_type": ai_data.get("issue_type"),
        "sub_issue_type": ai_data.get("sub_issue_type"),
        "ticket_type": (
            ai_data.get("ticket_type")
            if ai_data.get("ticket_type") in allowed_ticket_types
            else "incident"
        ),
    }


def get_tickets(
    db: Session,
    user: UserModel,
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    priority: str | None = None,
):
    """
    Retrieve tickets with optional filtering and pagination.

    - Admins can view all tickets
    - Regular users can only view their own tickets
    """

    query = db.query(TicketModel).filter(TicketModel.is_deleted == False)

    # Enforce ownership for non-admin users
    if user.role != "admin":
        query = query.filter(TicketModel.owner_id == user.id)

    if status:
        query = query.filter(TicketModel.status == status)

    if priority:
        query = query.filter(TicketModel.priority == priority)

    return (
        query.order_by(TicketModel.created_at.desc()).limit(limit).offset(offset).all()
    )


def get_ticket_by_id(db: Session, ticket_id: int, user: UserModel):
    """Retrieve a single ticket with access control."""

    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    _check_ticket_access(ticket, user)
    return ticket


def create_ticket(db: Session, ticket: TicketCreate, user: UserModel):
    """
    Create a new ticket and enrich it with AI-generated metadata.

    If AI processing fails, safe defaults are applied to ensure
    the system remains stable.
    """

    new_ticket = TicketModel(
        title=ticket.title,
        description=ticket.description,
        owner_id=user.id,
    )

    try:
        ai_data = analyze_ticket(ticket.title, ticket.description)
        logger.info("AI RAW OUTPUT: %s", ai_data)

        ai_data = _sanitize_ai_output(ai_data)
        logger.info("AI SANITIZED OUTPUT: %s", ai_data)

        # Apply AI fields dynamically
        for key, value in ai_data.items():
            setattr(new_ticket, key, value)

        # Ensure safe values before assignment
        category = new_ticket.category or "other"
        priority = new_ticket.priority or "medium"

    except Exception as e:
        logger.error("AI ERROR: %s", e)

        # Fallback defaults to maintain system reliability
        new_ticket.priority = "medium"
        new_ticket.status = "open"
        new_ticket.category = "other"
        new_ticket.ticket_type = "incident"

        category = new_ticket.category
        priority = new_ticket.priority

    # Assign technician AFTER AI (or fallback)
    assigned_tech = assign_technician(
        db,
        category,
        priority,
    )

    if assigned_tech:
        new_ticket.assigned_technician_id = assigned_tech.id

        # Increment technician load
        assigned_tech.current_ticket_count += 1
        db.add(assigned_tech)

        logger.info(
            "ASSIGNMENT: Ticket assigned to Tech %s | New Load: %s",
            assigned_tech.id,
            assigned_tech.current_ticket_count,
        )

    # Persist ticket
    db.add(new_ticket)
    db.commit()

    # Refresh both objects to reflect DB state
    db.refresh(new_ticket)

    if assigned_tech:
        db.refresh(assigned_tech)

    return new_ticket


def update_ticket_user(
    db: Session,
    ticket_id: int,
    updated_ticket: TicketUserUpdate,
    user: UserModel,
):
    """
    Allow users to update their own ticket content (title/description only).
    """

    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    _check_ticket_access(ticket, user)

    update_data = updated_ticket.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket


def update_ticket(
    db: Session,
    ticket_id: int,
    updated_ticket: TicketUpdate,
    user: UserModel,
):
    """
    Allow admins to fully update ticket fields including status,
    priority, and classification.
    """

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    # Capture previous state BEFORE update
    previous_status = ticket.status

    update_data = updated_ticket.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    # Handle lifecycle: decrement load when ticket is closed
    if (
        previous_status != "closed"
        and ticket.status == "closed"
        and ticket.assigned_technician
    ):
        tech = ticket.assigned_technician
        tech.current_ticket_count = max(0, tech.current_ticket_count - 1)
        db.add(tech)

        logger.info(
            "LOAD UPDATE: Ticket %s closed | Tech %s new load: %s",
            ticket.id,
            tech.id,
            tech.current_ticket_count,
        )

    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int, user: UserModel):
    """
    Soft delete a ticket.

    The ticket is not removed from the database, but marked as deleted.
    """

    ticket = _get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    _check_ticket_access(ticket, user)

    ticket.is_deleted = True

    db.commit()
    db.refresh(ticket)
    return ticket


from app.models.technician import TechnicianModel
from app.models.ticket import TicketModel


def assign_technician(db, category: str, priority: str):
    """
    Assigns technician based on:
    - Department match (with fallback)
    - Skill level vs required priority (with fallback)
    - Capacity
    - Load balancing
    """

    if not category:
        return None

    category = category.lower()

    # Priority → required level
    priority_map = {"low": 1, "medium": 2, "high": 3}

    required_level = priority_map.get(priority, 2)

    # Technician levels
    skill_map = {"junior": 1, "mid": 2, "senior": 3}

    # Ordered fallback levels
    fallback_levels = {
        3: [3, 2, 1],  # high
        2: [2, 1],  # medium
        1: [1],  # low
    }

    technicians = (
        db.query(TechnicianModel).filter(TechnicianModel.is_active == True).all()
    )

    def find_best_tech(tech_list, level_group):
        eligible = []

        for tech in tech_list:
            tech_level = skill_map.get((tech.skill_level or "").lower(), 1)

            # Skip if below required level
            if tech_level not in level_group:
                continue

            current_load = len([t for t in tech.tickets if t.status != "closed"])

            if current_load < tech.max_ticket_capacity:
                eligible.append((tech, current_load))

        if not eligible:
            return None

        return min(eligible, key=lambda x: x[1])[0]

    fallback_levels = {
        3: [[3]],
        2: [[2, 3], [3]],
        1: [[1, 2, 3]],
    }

    # Try department match FIRST
    dept_techs = [
        t for t in technicians if t.department and t.department.lower() == category
    ]

    # Try fallback levels within department
    for level_group in fallback_levels.get(required_level, [[2, 3]]):
        best = find_best_tech(dept_techs, level_group)
        if best:
            return best

    # Fallback to ANY department
    for level_group in fallback_levels.get(required_level, [[2, 3]]):
        best = find_best_tech(technicians, level_group)
        if best:
            return best

    return None
