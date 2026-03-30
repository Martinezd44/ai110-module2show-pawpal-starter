# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan daily care tasks for their pets using priority-based scheduling logic.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## What was built

### Backend — `pawpal_system.py`

Five classes power the scheduling logic:

| Class | Responsibility |
|---|---|
| `Owner` | Stores the owner's name, available daily minutes, and scheduling preferences |
| `Pet` | Stores pet info and owns its own task list via `add_task()` / `task_count()` |
| `Task` | Represents a single care task with priority, category, duration, start time, and recurrence |
| `Scheduler` | Sorts tasks by priority or time, fits them within the time budget, and detects conflicts |
| `DailyPlan` | Holds the result — scheduled tasks, skipped tasks, time used, and any conflicts |

Key methods:
- `Task.mark_complete()` — marks a task done
- `Task.renew()` — creates a fresh copy of a recurring task
- `Task.start_minutes()` / `Task.end_minutes()` — converts HH:MM to minutes for overlap detection
- `Scheduler.generate_plan(sort_by)` — generates the daily plan sorted by `"priority"` or `"time"`
- `Scheduler.detect_conflicts()` — flags tasks whose time windows overlap
- `DailyPlan.explain()` — returns a markdown summary of the plan and reasoning

### Streamlit UI — `app.py`

- Owner setup form with name, available time, and scheduling preferences (persisted in `st.session_state`)
- Multi-pet support — add as many pets as needed and switch between them
- Task form with title, duration, priority, category, start time, and recurrence options
- Live time budget counter showing minutes used vs. available
- Task list with pet and status filters (All / Pending / Completed)
- Mark task complete button that calls `task.mark_complete()`
- Schedule generation with sort toggle (priority or time)
- Results displayed with `st.metric`, `st.table`, `st.success`, `st.warning`, and `st.error`

### Tests — `tests/test_pawpal.py`

17 tests covering:
- Task completion (`mark_complete`)
- Task addition to a pet (`add_task`, `task_count`)
- Scheduler time budget enforcement
- Priority ordering
- Sort by time (chronological order, untimed tasks last)
- Recurring task renewal (`renew`)
- Conflict detection (same time, overlap, adjacent, one timed task)

## Project structure

```
pawpal_system.py      # All backend classes and logic
app.py                # Streamlit UI
main.py               # Terminal testing ground
tests/
  test_pawpal.py      # pytest test suite
class_diagram.md      # Mermaid.js UML class diagram
reflection.md         # Project reflection
requirements.txt      # Dependencies
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

## Running tests

```bash
python -m pytest tests/test_pawpal.py -v
```

## Running the terminal demo

```bash
python main.py
```
