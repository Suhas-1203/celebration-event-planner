"""Vendor checklist builder per event type."""

from .models import EventRequest, EventType

VENDOR_TEMPLATES: dict[EventType, dict[str, list[str]]] = {
    EventType.WEDDING: {
        "venue": ["Site visit", "Contract signed", "Deposit paid"],
        "catering": ["Tasting done", "Menu finalized", "Dietary needs confirmed"],
        "photography": ["Portfolio reviewed", "Booking confirmed", "Shot list shared"],
        "decor": ["Theme approved", "Florist booked", "Setup timeline agreed"],
    },
    EventType.BIRTHDAY: {
        "venue": ["Site visit", "Booking confirmed"],
        "cake": ["Design chosen", "Order placed", "Pickup/delivery confirmed"],
        "entertainment": ["Act booked", "Playlist shared"],
        "decor": ["Theme approved", "Balloons/decor ordered"],
    },
    EventType.COMMUNITY: {
        "permits": ["Application filed", "Permit received"],
        "logistics": ["Equipment booked", "Volunteers assigned", "Insurance confirmed"],
        "marketing": ["Poster designed", "Social media scheduled"],
    },
}


def build_checklist(req: EventRequest) -> dict[str, list[dict]]:
    """
    Return a checklist keyed by category, each item a dict with
    'item' (description) and 'status' (always 'todo' initially).
    """
    tpl = VENDOR_TEMPLATES[req.event_type]
    return {
        category: [{"item": item, "status": "todo"} for item in items]
        for category, items in tpl.items()
    }


def checklist_progress(checklist: dict[str, list[dict]]) -> dict[str, dict]:
    """
    Summarize progress: per category counts and overall percentage.
    Useful for the UI progress bar.
    """
    total = 0
    done = 0
    per_category: dict[str, dict] = {}
    for category, items in checklist.items():
        cat_total = len(items)
        cat_done = sum(1 for i in items if i.get("status") == "done")
        total += cat_total
        done += cat_done
        per_category[category] = {
            "done": cat_done,
            "total": cat_total,
            "pct": round(100 * cat_done / cat_total, 1) if cat_total else 0.0,
        }
    overall = round(100 * done / total, 1) if total else 0.0
    return {"overall_pct": overall, "categories": per_category}