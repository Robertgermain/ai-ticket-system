from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# 🔹 Shared base
class TicketBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5)

    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["open", "in_progress", "closed"] = "open"

    category: Optional[str] = None
    issue_type: Optional[str] = None
    sub_issue_type: Optional[str] = None

    ticket_type: Optional[Literal["incident", "request", "alert"]] = None


class TicketCreate(TicketBase):
    pass


# 🔹 Update ticket (partial updates)
class TicketUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, min_length=5)

    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["open", "in_progress", "closed"]] = None

    category: Optional[str] = None
    issue_type: Optional[str] = None
    sub_issue_type: Optional[str] = None

    ticket_type: Optional[Literal["incident", "request", "alert"]] = None


# 🔹 API response
class Ticket(BaseModel):
    id: int
    title: str
    description: str

    status: str
    priority: str

    category: Optional[str]
    issue_type: Optional[str]
    sub_issue_type: Optional[str]

    ticket_type: Optional[str]

    owner_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
