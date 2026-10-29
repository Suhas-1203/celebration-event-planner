"""Unit tests for the deterministic budget allocator."""

from datetime import date, timedelta

import pytest

from planner.budget import allocate_budget, per_guest_cost, validate_allocations
from planner.models import EventRequest, EventType


def _req(budget: float = 100000, guests: int = 100, et: EventType = EventType.WEDDING):
    return EventRequest(
        event_type=et,
        event_date=date.today() + timedelta(days=60),
        guest_count=guests,
        total_budget=budget,
    )


def test_allocations_sum_to_one():
    validate_allocations()


@pytest.mark.parametrize("et", list(EventType))
@pytest.mark.parametrize("budget", [1, 999, 100000, 9_999_999])
def test_budget_sums_exactly(et, budget):
    r = _req(budget=budget, et=et)
    b = allocate_budget(r)
    assert abs(sum(b.values()) - r.total_budget) < 0.01


@pytest.mark.parametrize("et", list(EventType))
def test_all_categories_positive(et):
    b = allocate_budget(_req(et=et))
    assert all(v > 0 for v in b.values())


def test_per_guest_cost():
    assert per_guest_cost(_req(budget=100000, guests=100)) == 1000.0


def test_per_guest_cost_rounding():
    assert per_guest_cost(_req(budget=100, guests=3)) == 33.33

def test_budget_allocation_error():
    from planner.budget import ALLOCATIONS, validate_allocations
    # Temporarily break the allocation to trigger the error
    ALLOCATIONS[EventType.WEDDING]["venue"] = 0.99
    with pytest.raises(AssertionError):
        validate_allocations()
    # Fix it back
    ALLOCATIONS[EventType.WEDDING]["venue"] = 0.25

def test_rounding_drift():
    # A budget that causes rounding drift with the percentages
    r = _req(budget=100.01, et=EventType.BIRTHDAY)
    b = allocate_budget(r)
    assert abs(sum(b.values()) - r.total_budget) < 0.01

def test_budget_allocation_error():
    from planner.budget import ALLOCATIONS, validate_allocations
    ALLOCATIONS[EventType.WEDDING]["venue"] = 0.99
    with pytest.raises(AssertionError):
        validate_allocations()
    ALLOCATIONS[EventType.WEDDING]["venue"] = 0.25

def test_rounding_drift():
    r = _req(budget=100.01, et=EventType.BIRTHDAY)
    b = allocate_budget(r)
    assert abs(sum(b.values()) - r.total_budget) < 0.01

def test_budget_allocation_error():
    from planner.budget import ALLOCATIONS, validate_allocations
    ALLOCATIONS[EventType.WEDDING]["venue"] = 0.99
    with pytest.raises(AssertionError):
        validate_allocations()
    ALLOCATIONS[EventType.WEDDING]["venue"] = 0.25

def test_rounding_drift():
    r = _req(budget=100.01, et=EventType.BIRTHDAY)
    b = allocate_budget(r)
    assert abs(sum(b.values()) - r.total_budget) < 0.01    