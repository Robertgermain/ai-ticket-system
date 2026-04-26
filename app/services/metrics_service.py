from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.ticket import TicketModel
from app.models.technician import TechnicianModel


def get_metrics(db: Session):
    """
    Returns system-wide metrics for tickets and technicians.
    """

    # Total tickets
    total_tickets = db.query(func.count(TicketModel.id)).scalar()

    # Open tickets
    open_tickets = (
        db.query(func.count(TicketModel.id))
        .filter(TicketModel.status != "closed")
        .scalar()
    )

    # Closed tickets
    closed_tickets = (
        db.query(func.count(TicketModel.id))
        .filter(TicketModel.status == "closed")
        .scalar()
    )

    # Tickets by category
    category_counts = (
        db.query(TicketModel.category, func.count(TicketModel.id))
        .group_by(TicketModel.category)
        .all()
    )

    tickets_by_category = {category: count for category, count in category_counts}

    # Technician workload
    technicians = db.query(TechnicianModel).all()

    technician_load = [
        {
            "id": tech.id,
            "name": f"{tech.first_name} {tech.last_name}",
            "department": tech.department,
            "active_tickets": tech.current_ticket_count,
            "capacity": tech.max_ticket_capacity,
        }
        for tech in technicians
    ]

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "closed_tickets": closed_tickets,
        "tickets_by_category": tickets_by_category,
        "technician_load": technician_load,
    }
