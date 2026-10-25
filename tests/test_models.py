"""Tests for Pydantic model validators."""

from datetime import date, timedelta
import pytest
from planner.models import EventRequest, EventType

def _req(**kwargs):
    defaults = dict(
        event_type=EventType.WEDDING,
        event_date=date.today() + timedelta(days=90),
        guest_count=50,
        total_budget=50000,
    )
    defaults.update(kwargs)
    return EventRequest(**defaults)

def test_control_chars_stripped():
    r = _req(vibe="Hello\x00World")
    assert "\x00" not in r.vibe

def test_currency_uppercased():
    r = _req(currency="usd")

def test_control_chars_stripped():
    r = _req(vibe="hello\x00world")
    assert "\x00" not in r.vibe