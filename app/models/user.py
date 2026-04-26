from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    role = Column(String(20), default="user", nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

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

    tickets = relationship(
        "TicketModel",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
