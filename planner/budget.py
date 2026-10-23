"""Deterministic budget allocation for event plans."""

from .models import EventRequest, EventType

# Percentages per event type. Each must sum to 1.0 exactly.
ALLOCATIONS: dict[EventType, dict[str, float]] = {
    EventType.WEDDING: {
        "venue": 0.25,
        "catering": 0.30,
        "decor": 0.12,
        "photography": 0.10,
        "attire": 0.08,
        "entertainment": 0.07,
        "misc": 0.08,
    },
    EventType.BIRTHDAY: {
        "venue": 0.20,
        "catering": 0.30,
        "cake": 0.10,
        "decor": 0.15,
        "entertainment": 0.15,
        "misc": 0.10,
    },
    EventType.COMMUNITY: {
        "venue": 0.20,
        "catering": 0.25,
        "logistics": 0.20,
        "marketing": 0.15,
        "permits": 0.10,
        "misc": 0.10,
    },
}


def validate_allocations() -> None:
    """Raise AssertionError if any category set does not sum to 1.0."""
    for event_type, alloc in ALLOCATIONS.items():
        total = sum(alloc.values())
        if abs(total - 1.0) > 1e-9:
            raise AssertionError(
                f"{event_type.value} allocations sum to {total}, expected 1.0"
            )


def allocate_budget(req: EventRequest) -> dict[str, float]:
    """
    Split total_budget across categories, returning amounts rounded to 2 dp.
    The sum of returned values is guaranteed to equal req.total_budget exactly
    (rounding drift is absorbed by the largest category).
    """
    alloc = ALLOCATIONS[req.event_type]
    result = {cat: round(req.total_budget * pct, 2) for cat, pct in alloc.items()}

    drift = round(req.total_budget - sum(result.values()), 2)
    if drift:
        biggest = max(result, key=result.get)
        result[biggest] = round(result[biggest] + drift, 2)

    return result


def per_guest_cost(req: EventRequest) -> float:
    """Total budget divided by guest count, rounded to 2 dp."""
    return round(req.total_budget / req.guest_count, 2)