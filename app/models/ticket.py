from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class TicketModel(Base):
    """
    ORM model representing a support ticket.

    Stores user-submitted issues along with AI-enriched metadata
    such as classification, priority, and summary.

    Supports soft deletion and ownership-based access control.
    """

    __tablename__ = "tickets"

    # Primary identifier
    id = Column(Integer, primary_key=True, index=True)

    # Core ticket fields
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), nullable=False)

    # AI-generated summary
    summary = Column(String(255), nullable=True)

    # Ticket lifecycle + priority
    status = Column(String(20), default="open", nullable=False, index=True)
    priority = Column(String(20), nullable=False, default="medium", index=True)

    # AI classification fields
    category = Column(String(50), nullable=True, index=True)
    issue_type = Column(String(50), nullable=True)
    sub_issue_type = Column(String(50), nullable=True)

    # Type of ticket (incident, request, alert)
    ticket_type = Column(String(20), nullable=True)

    # Audit timestamps (auto-managed by DB)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Soft delete flag (avoids hard deletion from DB)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Ownership (RBAC enforcement)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("UserModel", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket id={self.id} title={self.title} status={self.status}>"
