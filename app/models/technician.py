from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, timezone

from app.db.database import Base


class TechnicianModel(Base):
    """
    Represents a technician responsible for handling support tickets.

    This model supports:
    - AI-driven ticket routing
    - Skill-based assignment
    - Workload balancing
    """

    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)

    # Basic identity
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Organizational details
    role_title = Column(
        String(50),
        nullable=False,
        default="Service Technician",
    )  # e.g., Senior Technician

    department = Column(
        String(50),
        nullable=False,
        index=True,
    )  # e.g., network, hardware, security

    skill_level = Column(
        String(20),
        nullable=False,
        default="junior",
    )  # junior / mid / senior

    # ✅ Updated: use ARRAY instead of string
    skills = Column(
        ARRAY(String),
        nullable=True,
    )  # e.g., ["vpn", "firewall", "routing"]

    # Availability & workload
    is_active = Column(Boolean, default=True, nullable=False)

    current_ticket_count = Column(Integer, default=0, nullable=False)
    max_ticket_capacity = Column(Integer, default=5, nullable=False)

    # Relationships
    tickets = relationship(
        "TicketModel",
        back_populates="assigned_technician",
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<Technician id={self.id} email={self.email} dept={self.department}>"
