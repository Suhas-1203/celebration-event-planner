"""Unit tests for vendor checklist builder and progress summary."""

from datetime import date, timedelta

import pytest

from planner.models import EventRequest, EventType
from planner.vendors import VENDOR_TEMPLATES, build_checklist, checklist_progress


def _req(et: EventType):
    return EventRequest(
        event_type=et,
        event_date=date.today() + timedelta(days=90),
        guest_count=50,
        total_budget=50000,
    )


@pytest.mark.parametrize("et", list(EventType))
def test_checklist_categories_match_template(et):
    cl = build_checklist(_req(et))
    assert set(cl.keys()) == set(VENDOR_TEMPLATES[et].keys())


@pytest.mark.parametrize("et", list(EventType))
def test_every_item_starts_todo(et):
    for items in build_checklist(_req(et)).values():
        for it in items:
            assert it["status"] == "todo"
            assert isinstance(it["item"], str) and it["item"]


@pytest.mark.parametrize("et", list(EventType))
def test_item_counts_match_template(et):
    cl = build_checklist(_req(et))
    for cat, items in cl.items():
        assert len(items) == len(VENDOR_TEMPLATES[et][cat])


def test_progress_all_todo():
    cl = build_checklist(_req(EventType.WEDDING))
    p = checklist_progress(cl)
    assert p["overall_pct"] == 0.0
    assert all(c["done"] == 0 for c in p["categories"].values())


def test_progress_partial():
    cl = build_checklist(_req(EventType.WEDDING))
    # mark first item of first category as done
    first_cat = next(iter(cl))
    cl[first_cat][0]["status"] = "done"
    p = checklist_progress(cl)
    assert p["categories"][first_cat]["done"] == 1
    assert p["overall_pct"] > 0


def test_progress_complete():
    cl = build_checklist(_req(EventType.BIRTHDAY))
    for items in cl.values():
        for it in items:
            it["status"] = "done"
    p = checklist_progress(cl)
    assert p["overall_pct"] == 100.0


def test_progress_empty_checklist():
    p = checklist_progress({})
    assert p["overall_pct"] == 0.0
    assert p["categories"] == {}