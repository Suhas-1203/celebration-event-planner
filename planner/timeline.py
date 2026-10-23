"""Reverse-scheduled timeline generator."""

from datetime import date, timedelta

from .models import EventRequest, EventType

# (weeks_before_event, task_description), ordered from farthest to nearest.
TIMELINES: dict[EventType, list[tuple[int, str]]] = {
    EventType.WEDDING: [
        (52, "Set budget & draft guest list"),
        (40, "Book venue"),
        (32, "Book caterer & photographer"),
        (24, "Send save-the-dates"),
        (16, "Order attire & send invitations"),
        (8, "Confirm vendors & finalize menu"),
        (4, "Final headcount to caterer"),
        (1, "Rehearsal & final walkthrough"),
    ],
    EventType.BIRTHDAY: [
        (8, "Pick theme & draft guest list"),
        (6, "Book venue & order cake"),
        (4, "Send invitations"),
        (2, "Confirm catering & entertainment"),
        (1, "Final headcount & decor setup plan"),
    ],
    EventType.COMMUNITY: [
        (16, "Form organizing committee"),
        (12, "Book venue & apply for permits"),
        (8, "Arrange sponsors & marketing"),
        (4, "Confirm vendors & volunteers"),
        (1, "Logistics run-through"),
    ],
}


def generate_timeline(req: EventRequest) -> list[dict]:
    """
    Return tasks with absolute due dates and days remaining.
    Tasks are ordered from farthest-in-future to closest-to-event.
    """
    tasks = TIMELINES[req.event_type]
    today = date.today()
    out: list[dict] = []
    for weeks, task in tasks:
        due = req.event_date - timedelta(weeks=weeks)
        out.append(
            {
                "task": task,
                "due": due.isoformat(),
                "days_left": (due - today).days,
            }
        )
    return out