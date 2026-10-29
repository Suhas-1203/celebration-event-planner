"""Streamlit UI for the Celebration & Event Planner assistant."""

from datetime import date, timedelta

import streamlit as st

from planner.budget import allocate_budget, per_guest_cost
from planner.llm import generate_ideas
from planner.models import EventRequest, EventType
from planner.timeline import generate_timeline
from planner.vendors import build_checklist, checklist_progress
from planner.export import generate_markdown_export

st.set_page_config(page_title="Celebration & Event Planner", page_icon="🎉", layout="wide")

# --- ACCESSIBILITY: High contrast & Keyboard Focus ---
st.markdown(
    """
    <style>
    /* High contrast text */
    .stApp { color: #FAFAFA; }
    
    /* Fix dull checkbox labels */
    .stCheckbox label p { 
        color: #FAFAFA !important; 
        font-size: 1.05rem !important; 
    }
    
    /* Highly visible focus outlines for keyboard navigation */
    button:focus, input:focus, select:focus, textarea:focus {
        outline: 3px solid #FF4B4B !important;
        outline-offset: 2px !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Open the main semantic landmark
st.markdown('<main aria-label="Event Planner Main Content">', unsafe_allow_html=True)

st.title("🎉 Celebration & Event Planner")
st.caption("Plan weddings, birthdays, and community events with a budget breakdown, timeline, vendor checklist, and personalised ideas.")

if "plan_data" not in st.session_state:
    st.session_state.plan_data = None

with st.form("intake"):
    st.header("Event details", help="Enter your event parameters below.")
    
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
        guests = st.number_input(
            "Guest count", min_value=1, max_value=5000, value=100, step=10,
            help="Enter the expected number of attendees."
        )
        budget_amt = st.number_input(
            "Total budget", min_value=1000.0, max_value=10_000_000.0,
            value=200000.0, step=5000.0,
            help="Enter your total available budget."
        )

    vibe = st.text_input(
        "Vibe / style (optional)", max_chars=200,
        placeholder="e.g. Rustic outdoor garden party",
        help="Describe the aesthetic or theme."
    )
    dietary = st.text_input(
        "Dietary constraints (optional)", max_chars=200,
        placeholder="e.g. Vegetarian, nut-free",
        help="List any food allergies or preferences."
    )
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
        
        # EFFICIENCY: Calculate once
        budget_dict = allocate_budget(req)
        
        st.session_state.plan_data = {
            "request": req,
            "budget": budget_dict,
            "timeline": generate_timeline(req),
            "checklist": build_checklist(req),
            "ideas": generate_ideas(req, budget_dict),
        }
    except Exception as exc:
        st.error(f"Invalid input: {exc}")
        st.session_state.plan_data = None
        st.stop()

if st.session_state.plan_data:
    data = st.session_state.plan_data
    req = data["request"]

    st.divider()

    # ---------- Budget ----------
    st.header("💰 Budget breakdown", help="Allocation of your total budget based on event type.")
    st.metric("Per-guest cost", f"{req.currency} {per_guest_cost(req):,.2f}")
    st.table([{"Category": k.title(), "Amount": f"{req.currency} {v:,.2f}"} for k, v in data["budget"].items()])

    # ---------- Timeline ----------
    st.header("🗓 Timeline", help="Reverse-scheduled tasks leading up to your event.")
    st.table(data["timeline"])

    # ---------- Checklist ----------
    st.header("✅ Vendor checklist", help="Track your progress on essential vendor tasks.")
    checklist = data["checklist"]
    
    for cat, items in checklist.items():
        st.subheader(cat.title())
        for it in items:
            key = f"chk-{req.event_type.value}-{cat}-{it['item']}"
            if st.checkbox(it["item"], key=key, value=(it["status"] == "done")):
                it["status"] = "done"
            else:
                it["status"] = "todo"
                
    progress = checklist_progress(checklist)
    st.progress(progress["overall_pct"] / 100)
    st.caption(f"Overall progress: {progress['overall_pct']}%")

    # ---------- Ideas ----------
    st.header("💡 Personalised ideas", help="AI-generated creative suggestions.")
    for idea in data["ideas"]:
        st.write(f"- {idea}")

    # ---------- Export ----------
    st.divider()
    export_md = generate_markdown_export(req, data["budget"], data["timeline"], checklist, data["ideas"])
    st.download_button("Download plan (Markdown)", export_md, file_name="event-plan.md", mime="text/markdown")

# Close the main semantic landmark
st.markdown('</main>', unsafe_allow_html=True)