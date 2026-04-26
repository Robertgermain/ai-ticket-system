from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class TicketCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Short title summarizing the issue",
    )
    description: str = Field(
        ...,
        min_length=5,
        description="Detailed description of the issue provided by the user",
    )


class TicketUserUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Updated ticket title (user-editable)",
    )
    description: Optional[str] = Field(
        default=None,
        min_length=5,
        description="Updated ticket description (user-editable)",
    )


class TicketBase(BaseModel):
    priority: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Priority level of the ticket",
    )
    status: Literal["open", "in_progress", "closed"] = Field(
        default="open",
        description="Current status of the ticket",
    )

    category: Optional[str] = Field(
        default=None,
        max_length=50,
        description="High-level category (e.g., hardware, software, network)",
    )
    issue_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Specific issue classification (e.g., login_issue, device_failure)",
    )
    sub_issue_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="More granular classification of the issue",
    )

    ticket_type: Optional[Literal["incident", "request", "alert"]] = Field(
        default=None,
        description="Type of ticket (incident, request, or alert)",
    )


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Updated title of the ticket",
    )
    description: Optional[str] = Field(
        default=None,
        min_length=5,
        description="Updated description of the issue",
    )

    priority: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Updated priority level",
    )
    status: Optional[Literal["open", "in_progress", "closed"]] = Field(
        default=None,
        description="Updated ticket status",
    )

    category: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Updated category",
    )
    issue_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Updated issue type",
    )
    sub_issue_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Updated sub-issue classification",
    )

    ticket_type: Optional[Literal["incident", "request", "alert"]] = Field(
        default=None,
        description="Updated ticket type",
    )


class Ticket(BaseModel):
    id: int = Field(..., description="Unique ticket ID")
    title: str = Field(..., description="Ticket title")
    description: str = Field(..., description="Ticket description")

    summary: Optional[str] = Field(
        None,
        description="AI-generated summary of the ticket",
    )

    status: Literal["open", "in_progress", "closed"] = Field(
        ..., description="Current ticket status"
    )
    priority: Literal["low", "medium", "high"] = Field(
        ..., description="Priority level"
    )

    category: Optional[str] = Field(
        None,
        description="Ticket category",
    )
    issue_type: Optional[str] = Field(
        None,
        description="Issue classification",
    )
    sub_issue_type: Optional[str] = Field(
        None,
        description="Detailed issue classification",
    )

    ticket_type: Optional[Literal["incident", "request", "alert"]] = Field(
        None,
        description="Type of ticket",
    )

    owner_id: int = Field(..., description="ID of the user who owns the ticket")
    created_at: datetime = Field(
        ..., description="Timestamp when the ticket was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the ticket was last updated"
    )
    is_deleted: bool = Field(..., description="Soft delete flag")

    class Config:
        from_attributes = True
