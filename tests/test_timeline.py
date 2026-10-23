"""Unit tests for the reverse-scheduled timeline generator."""

from datetime import date, timedelta

import pytest

from planner.models import EventRequest, EventType
from planner.timeline import TIMELINES, generate_timeline


def _req(et: EventType, days_ahead: int = 400):
    return EventRequest(
        event_type=et,
        event_date=date.today() + timedelta(days=days_ahead),
        guest_count=50,
        total_budget=50000,
    )


@pytest.mark.parametrize("et", list(EventType))
def test_timeline_non_empty(et):
    assert len(generate_timeline(_req(et))) == len(TIMELINES[et])


@pytest.mark.parametrize("et", list(EventType))
def test_all_due_dates_before_event(et):
    r = _req(et)
    for item in generate_timeline(r):
        due = date.fromisoformat(item["due"])
        assert due < r.event_date


@pytest.mark.parametrize("et", list(EventType))
def test_tasks_ordered_farthest_first(et):
    tl = generate_timeline(_req(et))
    dues = [date.fromisoformat(t["due"]) for t in tl]
    assert dues == sorted(dues)


@pytest.mark.parametrize("et", list(EventType))
def test_days_left_consistent(et):
    tl = generate_timeline(_req(et))
    today = date.today()
    for item in tl:
        expected = (date.fromisoformat(item["due"]) - today).days
        assert item["days_left"] == expected


def test_every_task_has_required_keys():
    for item in generate_timeline(_req(EventType.WEDDING)):
        assert set(item.keys()) == {"task", "due", "days_left"}
        assert isinstance(item["task"], str) and item["task"]