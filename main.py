"""main.py — testing ground to verify PawPal+ scheduling logic in the terminal."""

from pawpal_system import Owner, Pet, Task, Scheduler


def run_schedule(owner: Owner, pet: Pet, tasks: list[Task]) -> None:
    print(f"\n{'='*45}")
    print(f"  Today's Schedule for {pet.name} ({pet.species})")
    print(f"  Owner: {owner.name} | Available: {owner.available_minutes} min")
    print(f"{'='*45}")

    scheduler = Scheduler(owner=owner, pet=pet, tasks=tasks)
    plan = scheduler.generate_plan()

    if plan.scheduled_tasks:
        print("\n Scheduled Tasks:")
        for task in plan.scheduled_tasks:
            status = "[HIGH]" if task.priority == "high" else f"[{task.priority.upper()}]"
            print(f"   {status} {task.title} — {task.duration_minutes} min ({task.category})")
    else:
        print("\n  No tasks could be scheduled.")

    if plan.skipped_tasks:
        print("\n Skipped (not enough time):")
        for task in plan.skipped_tasks:
            print(f"   - {task.title} — {task.duration_minutes} min")

    if plan.conflicts:
        print("\n ⚠ Time conflicts:")
        for a, b in plan.conflicts:
            print(f"   {a.title} ({a.start_time}) overlaps {b.title} ({b.start_time})")

    print(f"\n Total time used: {plan.total_minutes} / {owner.available_minutes} min")
    print(f"{'='*45}\n")


if __name__ == "__main__":
    # --- Owner ---
    jordan = Owner(name="Jordan", available_minutes=90, preferences=["no late tasks"])

    # --- Pets ---
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna  = Pet(name="Luna",  species="cat", age=5)

    # --- Tasks for Mochi (dog) ---
    mochi_tasks = [
        Task(title="Morning walk",    duration_minutes=30, priority="high",   category="walk"),
        Task(title="Breakfast",       duration_minutes=10, priority="high",   category="feeding"),
        Task(title="Flea medication", duration_minutes=5,  priority="medium", category="meds"),
        Task(title="Fetch/play time", duration_minutes=20, priority="low",    category="enrichment"),
        Task(title="Bath time",       duration_minutes=40, priority="low",    category="grooming"),
    ]

    # --- Tasks for Luna (cat) ---
    luna_tasks = [
        Task(title="Breakfast",          duration_minutes=10, priority="high",   category="feeding"),
        Task(title="Litter box cleaning", duration_minutes=10, priority="high",   category="grooming"),
        Task(title="Hairball treatment",  duration_minutes=5,  priority="medium", category="meds"),
        Task(title="Laser pointer play",  duration_minutes=15, priority="low",    category="enrichment"),
    ]

    # --- Run schedules ---
    run_schedule(jordan, mochi, mochi_tasks)
    run_schedule(jordan, luna, luna_tasks)
