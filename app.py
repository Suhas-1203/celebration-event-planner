"""Streamlit UI for the Celebration & Event Planner assistant."""

from datetime import date, timedelta

import streamlit as st

from planner.budget import allocate_budget, per_guest_cost
from planner.llm import generate_ideas
from planner.models import EventRequest, EventType
from planner.timeline import generate_timeline
from planner.vendors import build_checklist, checklist_progress

st.set_page_config(page_title="Celebration & Event Planner", page_icon="🎉", layout="wide")

st.title("🎉 Celebration & Event Planner")
st.caption(
    "Plan weddings, birthdays, and community events with a budget breakdown, "
    "timeline, vendor checklist, and personalised ideas."
)

# Initialize session state for the plan
if "plan_data" not in st.session_state:
    st.session_state.plan_data = None

with st.form("intake"):
    st.subheader("Event details")
    col1, col2 = st.columns(2)
    with col1:
        et_label = st.selectbox(
            "Event type", [e.value.title() for e in EventType], index=0,
            help="Choose the kind of event you are planning.",
        )
        ed = st.date_input(
            "Event date", value=date.today() + timedelta(days=90),
            help="Must be a future date.",
        )
    with col2:
        guests = st.number_input("Guest count", min_value=1, max_value=5000, value=100, step=10)
        budget_amt = st.number_input(
            "Total budget", min_value=1000.0, max_value=10_000_000.0,
            value=200000.0, step=5000.0,
        )

    vibe = st.text_input("Vibe / style (optional)", max_chars=200,
                         placeholder="e.g. Rustic outdoor garden party")
    dietary = st.text_input("Dietary constraints (optional)", max_chars=200,
                            placeholder="e.g. Vegetarian, nut-free")
    submitted = st.form_submit_button("Generate plan", use_container_width=True)

if submitted:
    try:
        req = EventRequest(
            event_type=EventType(et_label.lower()),
            event_date=ed,
            guest_count=guests,
            total_budget=budget_amt,
            vibe=vibe,
            dietary=dietary,
        )
        # Generate and save to session state
        st.session_state.plan_data = {
            "request": req,
            "budget": allocate_budget(req),
            "timeline": generate_timeline(req),
            "checklist": build_checklist(req),
            "ideas": generate_ideas(req, allocate_budget(req)),
        }
    except Exception as exc:
        st.error(f"Invalid input: {exc}")
        st.session_state.plan_data = None
        st.stop()

# Only display if plan data exists in memory
if st.session_state.plan_data:
    data = st.session_state.plan_data
    req = data["request"]

    st.divider()

    # ---------- Budget ----------
    st.header("💰 Budget breakdown")
    st.metric("Per-guest cost", f"{req.currency} {per_guest_cost(req):,.2f}")
    st.table(
        [{"Category": k.title(), "Amount": f"{req.currency} {v:,.2f}"}
         for k, v in data["budget"].items()]
    )

    # ---------- Timeline ----------
    st.header("🗓 Timeline")
    st.table(data["timeline"])

    # ---------- Checklist ----------
    st.header("✅ Vendor checklist")
    checklist = data["checklist"]
    
    # We use columns to layout the checklist nicely
    for cat, items in checklist.items():
        st.subheader(cat.title())
        for it in items:
            key = f"chk-{req.event_type.value}-{cat}-{it['item']}"
            # If the widget key is true, update the underlying dict
            if st.checkbox(it["item"], key=key, value=(it["status"] == "done")):
                it["status"] = "done"
            else:
                it["status"] = "todo"
                
    # Update progress
    progress = checklist_progress(checklist)
    st.progress(progress["overall_pct"] / 100)
    st.caption(f"Overall progress: {progress['overall_pct']}%")

    # ---------- Ideas ----------
    st.header("💡 Personalised ideas")
    for idea in data["ideas"]:
        st.write(f"- {idea}")

    # ---------- Export ----------
    st.divider()
    export = (
        f"# Event Plan — {req.event_type.value.title()}\n"
        f"Date: {req.event_date}\nGuests: {req.guest_count}\n"
        f"Budget: {req.currency} {req.total_budget:,.2f}\n\n"
        f"## Budget\n" + "\n".join(f"- {k}: {v}" for k, v in data["budget"].items())
        + "\n\n## Timeline\n"
        + "\n".join(f"- {t['due']}: {t['task']}" for t in data["timeline"])
        + "\n\n## Checklist\n"
        + "\n".join(
            f"- [{it['status']}] {cat}: {it['item']}"
            for cat, items in checklist.items() for it in items
        )
        + "\n\n## Ideas\n"
        + "\n".join(f"- {i}" for i in data["ideas"])
    )
    st.download_button("Download plan (Markdown)", export,
                       file_name="event-plan.md", mime="text/markdown")