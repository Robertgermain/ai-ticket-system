from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), nullable=False)

    summary = Column(String(255), nullable=True)

    status = Column(String(20), default="open", nullable=False, index=True)
    priority = Column(String(20), nullable=False, default="medium", index=True)

    category = Column(String(50), nullable=True, index=True)
    issue_type = Column(String(50), nullable=True)
    sub_issue_type = Column(String(50), nullable=True)

    ticket_type = Column(String(20), nullable=True)

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

    is_deleted = Column(Boolean, default=False, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("UserModel", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket id={self.id} title={self.title} status={self.status}>"
