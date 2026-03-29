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


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"   # "low" | "medium" | "high"
    category: str = "general"  # walk | feeding | meds | grooming | enrichment
    completed: bool = False

    def priority_value(self) -> int:
        """Lower number = higher priority."""
        return PRIORITY_ORDER.get(self.priority, 1)


@dataclass
class DailyPlan:
    scheduled_tasks: list[Task]
    skipped_tasks: list[Task]
    total_minutes: int

    def explain(self) -> str:
        """Return a human-readable summary of the plan and reasoning."""
        lines = []
        lines.append(
            f"Scheduled {len(self.scheduled_tasks)} task(s) "
            f"using {self.total_minutes} minute(s) of available time.\n"
        )

        if self.scheduled_tasks:
            lines.append("**Included tasks (sorted by priority):**")
            for task in self.scheduled_tasks:
                lines.append(
                    f"- {task.title} [{task.priority}] — {task.duration_minutes} min ({task.category})"
                )

        if self.skipped_tasks:
            lines.append("\n**Skipped (not enough time remaining):**")
            for task in self.skipped_tasks:
                lines.append(
                    f"- {task.title} [{task.priority}] — {task.duration_minutes} min"
                )

        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def generate_plan(self) -> DailyPlan:
        """Sort tasks by priority and fit as many as possible within available time."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority_value())
        scheduled: list[Task] = []
        skipped: list[Task] = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                scheduled.append(task)
                time_used += task.duration_minutes
            else:
                skipped.append(task)

        return DailyPlan(
            scheduled_tasks=scheduled,
            skipped_tasks=skipped,
            total_minutes=time_used,
        )
