"""Validated input models for the Celebration & Event Planner."""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class EventType(str, Enum):
    """Supported event verticals."""

    WEDDING = "wedding"
    BIRTHDAY = "birthday"
    COMMUNITY = "community"


class EventRequest(BaseModel):
    """User-supplied event intake. All fields are validated on construction."""

    event_type: EventType
    event_date: date
    guest_count: int = Field(gt=0, le=5000, description="Number of guests")
    total_budget: float = Field(gt=0, le=10_000_000, description="Total budget")
    currency: str = Field(default="INR", min_length=3, max_length=3)
    vibe: str = Field(default="", max_length=200)
    dietary: str = Field(default="", max_length=200)

    @field_validator("event_date")
    @classmethod
    def _future_date(cls, v: date) -> date:
        if v <= date.today():
            raise ValueError("event_date must be in the future")
        return v

    @field_validator("vibe", "dietary")
    @classmethod
    def _strip_control(cls, v: str) -> str:
        # remove non-printable characters, cap length defensively
        return "".join(c for c in v if c.isprintable())[:200]

    @field_validator("currency")
    @classmethod
    def _upper_currency(cls, v: str) -> str:
        return v.upper()


class PlanResult(BaseModel):
    """Structured output of the planner for one request."""

    request: EventRequest
    budget: dict[str, float]
    per_guest_cost: float
    timeline: list[dict]
    checklist: dict[str, list[dict]]
    ideas: list[str]