from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class UserModel(Base):
    """
    ORM model representing an application user.

    Stores authentication credentials, profile information,
    and role-based access control (RBAC) data.

    Users can own multiple tickets and may have different
    permission levels (e.g., admin vs standard user).
    """

    __tablename__ = "users"

    # Primary identifier
    id = Column(Integer, primary_key=True, index=True)

    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Role-based access control
    role = Column(String(20), default="user", nullable=False)

    # Basic profile information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # Account status (used for soft deactivation)
    is_active = Column(Boolean, default=True, nullable=False)

    # Audit timestamps
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

    # Relationship to tickets (one-to-many)
    tickets = relationship(
        "TicketModel",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
