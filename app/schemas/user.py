from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime


class UserBase(BaseModel):
    """Shared user fields used across multiple schemas."""

    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="User's first name",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="User's last name",
    )


class UserCreate(UserBase):
    """Schema for registering a new user."""

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (min 8 characters)",
    )


class AdminUserCreate(UserCreate):
    """Schema for admin-created users (includes role assignment)."""

    role: Literal["admin", "user"] = Field(
        default="user",
        description="Role assigned to the user (admin or user)",
    )


class UserUpdate(BaseModel):
    """
    Schema for updating user profile information.

    Restricted to non-sensitive fields (e.g., no role or account status).
    """

    first_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Updated first name",
    )
    last_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Updated last name",
    )


class UserRoleUpdate(BaseModel):
    """Schema for admin-only role updates."""

    role: Literal["admin", "user"] = Field(
        ...,
        description="New role for the user",
    )


class UserResponse(UserBase):
    """Response schema representing a user returned by the API."""

    id: int = Field(..., description="Unique user ID")
    role: Literal["admin", "user"] = Field(..., description="User role")
    is_active: bool = Field(..., description="Indicates if the user is active")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the user was last updated"
    )

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication responses containing JWT tokens."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (bearer)")
    expires_in: Optional[int] = Field(
        default=None,
        description="Token expiration time in seconds",
    )
