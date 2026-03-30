import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Owner Setup
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("⚙️ Owner Setup", expanded="owner" not in st.session_state):
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input(
        "Available time today (minutes)", min_value=10, max_value=480, value=120
    )
    preferences = st.multiselect(
        "Scheduling preferences",
        options=["no low priority tasks", "meds first"],
        help=(
            '"no low priority tasks" removes low-priority items before scheduling. '
            '"meds first" bumps medication tasks above all other priorities.'
        ),
    )
    if st.button("Save Owner"):
        st.session_state.owner = Owner(
            name=owner_name,
            available_minutes=int(available_minutes),
            preferences=preferences,
        )
        st.success(f"Saved — {owner_name}, {available_minutes} min available.")

if "owner" not in st.session_state:
    st.info("Fill in owner info above and click **Save Owner** to continue.")
    st.stop()

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Pet Management
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Pets")

if "pets" not in st.session_state:
    st.session_state.pets: list[Pet] = []

with st.form("add_pet_form"):
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with pc2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with pc3:
        pet_age = st.number_input("Age", min_value=0, max_value=30, value=3)

    if st.form_submit_button("Add Pet"):
        name = pet_name.strip()
        if name in [p.name for p in st.session_state.pets]:
            st.warning(f"A pet named '{name}' already exists.")
        elif not name:
            st.warning("Pet name cannot be blank.")
        else:
            st.session_state.pets.append(Pet(name=name, species=species, age=int(pet_age)))
            st.success(f"Added {name}!")

if not st.session_state.pets:
    st.info("Add at least one pet to continue.")
    st.stop()

pet_names = [p.name for p in st.session_state.pets]
active_pet_name = st.selectbox("Active pet (tasks are added here)", pet_names)
active_pet: Pet = next(p for p in st.session_state.pets if p.name == active_pet_name)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Task Management
# ─────────────────────────────────────────────────────────────────────────────
st.subheader(f"Tasks — {active_pet.name}")

# ── Add task form ─────────────────────────────────────────────────────────────
with st.form("add_task_form"):
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        task_title = st.text_input("Task title", value="Morning walk")
    with tc2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with tc3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    tc4, tc5, tc6, tc7 = st.columns(4)
    with tc4:
        category = st.selectbox(
            "Category",
            ["general", "walk", "feeding", "meds", "grooming", "enrichment"],
        )
    with tc5:
        start_time_input = st.text_input("Start time (HH:MM)", placeholder="08:00")
    with tc6:
        recurring = st.checkbox("Recurring?")
    with tc7:
        recurrence = st.selectbox("Recurrence", ["daily", "weekly"])

    if st.form_submit_button("Add Task"):
        error: str | None = None
        clean_start: str | None = start_time_input.strip() or None

        # Validate HH:MM format
        if clean_start:
            try:
                parts = clean_start.split(":")
                h, m = int(parts[0]), int(parts[1])
                if not (0 <= h <= 23 and 0 <= m <= 59):
                    raise ValueError
            except (ValueError, IndexError):
                error = "Start time must be in HH:MM format (e.g. 08:30)."

        # Duplicate title check
        if not error and task_title.strip() in [t.title for t in active_pet.tasks]:
            error = f"'{task_title}' is already in {active_pet.name}'s task list."

        if error:
            st.warning(error)
        else:
            active_pet.add_task(Task(
                title=task_title.strip(),
                duration_minutes=int(duration),
                priority=priority,
                category=category,
                start_time=clean_start,
                recurring=recurring,
                recurrence=recurrence if recurring else "daily",
            ))
            st.success(f"Added: {task_title}")

# ── Live time-remaining counter ───────────────────────────────────────────────
all_mins = sum(t.duration_minutes for t in active_pet.tasks)
budget = st.session_state.owner.available_minutes
remaining_budget = budget - all_mins

if remaining_budget >= 0:
    st.info(
        f"**Time budget:** {all_mins} min planned / {budget} min available "
        f"— **{remaining_budget} min remaining**"
    )
else:
    st.warning(
        f"**Time budget:** {all_mins} min planned / {budget} min available "
        f"— **{abs(remaining_budget)} min over budget**"
    )

# ── Task list with pet & status filters ──────────────────────────────────────
st.markdown("#### Task List")

if any(p.tasks for p in st.session_state.pets):
    fc1, fc2 = st.columns(2)
    with fc1:
        pet_filter = st.selectbox(
            "Filter by pet", ["All pets"] + pet_names, key="pet_filter"
        )
    with fc2:
        status_filter = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed"], key="status_filter"
        )

    # Collect rows based on pet filter
    if pet_filter == "All pets":
        rows = [(p.name, t) for p in st.session_state.pets for t in p.tasks]
    else:
        fp = next(p for p in st.session_state.pets if p.name == pet_filter)
        rows = [(fp.name, t) for t in fp.tasks]

    # Apply status filter
    if status_filter == "Pending":
        rows = [(pn, t) for pn, t in rows if not t.completed]
    elif status_filter == "Completed":
        rows = [(pn, t) for pn, t in rows if t.completed]

    if rows:
        st.table([
            {
                "pet": pn,
                "title": t.title,
                "min": t.duration_minutes,
                "priority": t.priority,
                "category": t.category,
                "start": t.start_time or "—",
                "recurs": f"↻ {t.recurrence}" if t.recurring else "—",
                "status": "✓ done" if t.completed else "pending",
            }
            for pn, t in rows
        ])
    else:
        st.caption("No tasks match the current filter.")

    # ── Mark task complete ────────────────────────────────────────────────────
    pending = [t for t in active_pet.tasks if not t.completed]
    if pending:
        mc1, mc2 = st.columns([3, 1])
        with mc1:
            to_complete = st.selectbox(
                "Mark task as complete",
                [t.title for t in pending],
                key="complete_selector",
            )
        with mc2:
            st.write("")
            st.write("")
            if st.button("✓ Done"):
                next(t for t in active_pet.tasks if t.title == to_complete).mark_complete()
                st.rerun()
else:
    st.caption("No tasks yet. Add one above.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Schedule Generation
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Generate Schedule")

sort_by = st.radio(
    "Sort output by",
    ["priority", "time"],
    horizontal=True,
    help=(
        '"priority" keeps high-priority tasks first. '
        '"time" orders by start time — tasks without a set time appear last.'
    ),
)

PRIORITY_BADGE = {"high": "🔴 high", "medium": "🟡 medium", "low": "🟢 low"}

if st.button("Generate Schedule"):
    pending_tasks = [t for t in active_pet.tasks if not t.completed]

    if not pending_tasks:
        st.warning(f"No pending tasks found for {active_pet.name}. Add tasks above first.")
    else:
        scheduler = Scheduler(
            owner=st.session_state.owner,
            pet=active_pet,
            tasks=pending_tasks,
        )
        plan = scheduler.generate_plan(sort_by=sort_by)

        # ── Summary metrics ───────────────────────────────────────────────────
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Scheduled", f"{len(plan.scheduled_tasks)} tasks")
        m2.metric("Time used", f"{plan.total_minutes} min")
        m3.metric("Available", f"{st.session_state.owner.available_minutes} min")
        m4.metric("Skipped", f"{len(plan.skipped_tasks)} tasks")

        # ── Conflict alerts ───────────────────────────────────────────────────
        if plan.conflicts:
            st.error(f"⚠️ {len(plan.conflicts)} time conflict(s) detected — review start times.")
            for a, b in plan.conflicts:
                st.warning(
                    f"**{a.title}** ({a.start_time}, {a.duration_minutes} min) "
                    f"overlaps **{b.title}** ({b.start_time}, {b.duration_minutes} min)"
                )
        else:
            st.success(f"Schedule ready for {active_pet.name} — no conflicts detected!")

        # ── Scheduled tasks table ─────────────────────────────────────────────
        if plan.scheduled_tasks:
            st.markdown("#### Scheduled Tasks")
            st.table([
                {
                    "title":    t.title,
                    "priority": PRIORITY_BADGE.get(t.priority, t.priority),
                    "category": t.category,
                    "start":    t.start_time or "—",
                    "duration": f"{t.duration_minutes} min",
                    "recurs":   f"↻ {t.recurrence}" if t.recurring else "—",
                }
                for t in plan.scheduled_tasks
            ])

        # ── Skipped tasks ─────────────────────────────────────────────────────
        if plan.skipped_tasks:
            st.markdown("#### Skipped Tasks")
            st.caption("These tasks did not fit within the available time budget.")
            st.table([
                {
                    "title":    t.title,
                    "priority": PRIORITY_BADGE.get(t.priority, t.priority),
                    "duration": f"{t.duration_minutes} min",
                    "reason":   "over time budget",
                }
                for t in plan.skipped_tasks
            ])