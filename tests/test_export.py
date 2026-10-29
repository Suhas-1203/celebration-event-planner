from datetime import date, timedelta
from planner.export import generate_markdown_export
from planner.models import EventRequest, EventType

def test_markdown_export():
    req = EventRequest(event_type=EventType.WEDDING, event_date=date.today() + timedelta(days=90), guest_count=50, total_budget=50000)
    budget = {"venue": 10000.0}
    timeline = [{"task": "Book", "due": "2026-01-01", "days_left": 10}]
    checklist = {"venue": [{"item": "Visit", "status": "todo"}]}
    ideas = ["Idea 1"]
    
    md = generate_markdown_export(req, budget, timeline, checklist, ideas)
    
    assert "# Event Plan" in md
    assert "- venue: 10000.0" in md
    assert "- 2026-01-01: Book" in md
    assert "- [todo] venue: Visit" in md
    assert "- Idea 1" in md