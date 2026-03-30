"""PawPal+ backend system — Owner, Pet, Task, Scheduler, DailyPlan."""

from dataclasses import dataclass, field


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Owner:
    name: str
    available_minutes: int = 120
    preferences: list[str] = field(default_factory=list)


@dataclass
class Pet:
    name: str
    species: str = "dog"
    age: int = 1
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"    # "low" | "medium" | "high"
    category: str = "general"   # walk | feeding | meds | grooming | enrichment
    completed: bool = False
    recurring: bool = False
    recurrence: str = "daily"   # "daily" | "weekly"
    start_time: str | None = None  # "HH:MM" optional

    def priority_value(self) -> int:
        """Lower number = higher priority."""
        return PRIORITY_ORDER.get(self.priority, 1)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def start_minutes(self) -> int | None:
        """Return start time as total minutes from midnight, or None."""
        if self.start_time is None:
            return None
        h, m = map(int, self.start_time.split(":"))
        return h * 60 + m

    def end_minutes(self) -> int | None:
        """Return end time as total minutes from midnight, or None."""
        start = self.start_minutes()
        return None if start is None else start + self.duration_minutes


@dataclass
class DailyPlan:
    scheduled_tasks: list[Task]
    skipped_tasks: list[Task]
    total_minutes: int
    conflicts: list[tuple["Task", "Task"]] = field(default_factory=list)

    def explain(self) -> str:
        """Return a human-readable Markdown summary of the plan and reasoning."""
        lines: list[str] = []
        lines.append(
            f"Scheduled **{len(self.scheduled_tasks)}** task(s) "
            f"using **{self.total_minutes} min** of available time.\n"
        )

        if self.conflicts:
            lines.append("⚠️ **Time conflicts detected:**")
            for a, b in self.conflicts:
                lines.append(
                    f"- **{a.title}** ({a.start_time}, {a.duration_minutes} min) overlaps "
                    f"**{b.title}** ({b.start_time}, {b.duration_minutes} min)"
                )
            lines.append("")

        if self.scheduled_tasks:
            lines.append("**Scheduled tasks:**")
            for task in self.scheduled_tasks:
                time_str = f" @ {task.start_time}" if task.start_time else ""
                recur_str = f" ↻ {task.recurrence}" if task.recurring else ""
                done_str = " ✓" if task.completed else ""
                lines.append(
                    f"- **{task.title}** [{task.priority}]{time_str} — "
                    f"{task.duration_minutes} min ({task.category}){recur_str}{done_str}"
                )

        if self.skipped_tasks:
            lines.append("\n**Skipped (not enough time):**")
            for task in self.skipped_tasks:
                lines.append(
                    f"- {task.title} [{task.priority}] — {task.duration_minutes} min"
                )

        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]):
        """Initialize the scheduler with an owner, a pet, and a list of tasks."""
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    # ── Conflict detection ────────────────────────────────────────────────────

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose explicit time windows overlap."""
        timed = [t for t in tasks if t.start_time is not None]
        conflicts: list[tuple[Task, Task]] = []
        for i, a in enumerate(timed):
            for b in timed[i + 1 :]:
                a_s, a_e = a.start_minutes(), a.end_minutes()
                b_s, b_e = b.start_minutes(), b.end_minutes()
                # Standard interval-overlap test (all values are int here)
                if a_s < b_e and b_s < a_e:  # type: ignore[operator]
                    conflicts.append((a, b))
        return conflicts

    # ── Priority helpers ──────────────────────────────────────────────────────

    def _effective_priority(self, task: Task) -> int:
        """Return sort key for a task, respecting owner scheduling preferences.

        'meds first' bumps medication tasks above high-priority tasks (key = -1).
        """
        if "meds first" in self.owner.preferences and task.category == "meds":
            return -1
        return task.priority_value()

    # ── Plan generation ───────────────────────────────────────────────────────

    def generate_plan(self, sort_by: str = "priority") -> DailyPlan:
        """Fit tasks greedily within available time, respecting priority integrity.

        Priority integrity rule: a lower-priority task is not scheduled if a
        higher-priority task was skipped AND would fit in the same remaining
        time slot — preventing low-priority tasks from sneaking in ahead of
        skipped-but-still-fittable higher-priority ones.

        sort_by:
            "priority" — output preserves priority order (default).
            "time"     — output is sorted by start_time (tasks without a
                         start_time appear last, ordered by priority).
        """
        no_low = "no low priority tasks" in self.owner.preferences

        candidates = [t for t in self.tasks if not (no_low and t.priority == "low")]
        sorted_tasks = sorted(candidates, key=self._effective_priority)

        scheduled: list[Task] = []
        skipped: list[Task] = []
        time_used = 0

        for task in sorted_tasks:
            remaining = self.owner.available_minutes - time_used
            if task.duration_minutes <= remaining:
                # Priority-integrity check: don't fill this slot with a lower-priority
                # task when a higher-priority skipped task would also fit here.
                blocks = any(
                    self._effective_priority(s) < self._effective_priority(task)
                    and s.duration_minutes <= remaining
                    for s in skipped
                )
                if blocks:
                    skipped.append(task)
                else:
                    scheduled.append(task)
                    time_used += task.duration_minutes
            else:
                skipped.append(task)

        if sort_by == "time":
            scheduled.sort(
                key=lambda t: (t.start_time or "99:99", self._effective_priority(t))
            )

        return DailyPlan(
            scheduled_tasks=scheduled,
            skipped_tasks=skipped,
            total_minutes=time_used,
            conflicts=self.detect_conflicts(scheduled),
        )