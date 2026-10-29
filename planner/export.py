"""Markdown export logic."""

from .models import EventRequest

def generate_markdown_export(req: EventRequest, budget: dict, timeline: list, checklist: dict, ideas: list) -> str:
    """Formats the entire plan into a downloadable Markdown string."""
    export = (
        f"# Event Plan — {req.event_type.value.title()}\n"
        f"Date: {req.event_date}\nGuests: {req.guest_count}\n"
        f"Budget: {req.currency} {req.total_budget:,.2f}\n\n"
        f"## Budget\n" + "\n".join(f"- {k}: {v}" for k, v in budget.items())
        + "\n\n## Timeline\n"
        + "\n".join(f"- {t['due']}: {t['task']}" for t in timeline)
        + "\n\n## Checklist\n"
        + "\n".join(
            f"- [{it['status']}] {cat}: {it['item']}"
            for cat, items in checklist.items() for it in items
        )
        + "\n\n## Ideas\n"
        + "\n".join(f"- {i}" for i in ideas)
    )
    return export