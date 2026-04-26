from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime


class TechnicianBase(BaseModel):
    """Shared technician fields."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Technician's first name",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Technician's last name",
    )
    email: EmailStr = Field(..., description="Technician email address")

    role_title: str = Field(
        default="Service Technician",
        max_length=50,
        description="Job title (e.g., Service Technician, Senior Technician)",
    )

    department: str = Field(
        ...,
        max_length=50,
        description="Primary department (e.g., network, hardware, security)",
    )

    skill_level: Literal["junior", "mid", "senior"] = Field(
        default="junior",
        description="Technician experience level",
    )

    skills: Optional[List[str]] = Field(
        default=None,
        description="List of technician skills (e.g., ['vpn', 'firewall'])",
    )


class TechnicianCreate(TechnicianBase):
    """Schema for creating a new technician."""

    max_ticket_capacity: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum number of concurrent tickets the technician can handle",
    )


class TechnicianUpdate(BaseModel):
    """
    Schema for updating technician details.

    All fields are optional to support partial updates.
    """

    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None

    role_title: Optional[str] = Field(default=None, max_length=50)
    department: Optional[str] = Field(default=None, max_length=50)
    skill_level: Optional[Literal["junior", "mid", "senior"]] = None

    skills: Optional[List[str]] = None

    is_active: Optional[bool] = Field(
        default=None,
        description="Whether the technician is active and can receive tickets",
    )

    max_ticket_capacity: Optional[int] = Field(
        default=None,
        ge=1,
        le=50,
        description="Updated maximum ticket capacity",
    )


class TechnicianResponse(TechnicianBase):
    """Response schema returned by the API."""

    id: int = Field(..., description="Unique technician ID")

    is_active: bool = Field(..., description="Indicates if technician is active")

    current_ticket_count: int = Field(
        ..., description="Number of tickets currently assigned"
    )
    max_ticket_capacity: int = Field(
        ..., description="Maximum number of concurrent tickets"
    )

    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
