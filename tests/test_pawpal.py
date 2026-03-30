"""Tests for PawPal+ core logic."""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


# ── Task Completion ────────────────────────────────────────────────────────────

def test_task_starts_incomplete():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    task.mark_complete()
    assert task.completed is True


def test_mark_complete_is_idempotent():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    task.mark_complete()
    task.mark_complete()
    assert task.completed is True


# ── Task Addition to Pet ───────────────────────────────────────────────────────

def test_pet_starts_with_no_tasks():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert pet.task_count() == 0


def test_adding_one_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(title="Breakfast", duration_minutes=10, priority="high")
    pet.add_task(task)
    assert pet.task_count() == 1


def test_adding_multiple_tasks_increases_count():
    pet = Pet(name="Luna", species="cat", age=5)
    pet.add_task(Task(title="Breakfast",       duration_minutes=10, priority="high"))
    pet.add_task(Task(title="Litter box",      duration_minutes=10, priority="high"))
    pet.add_task(Task(title="Laser pointer",   duration_minutes=15, priority="low"))
    assert pet.task_count() == 3


def test_added_task_is_stored_on_pet():
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(title="Evening walk", duration_minutes=20, priority="medium")
    pet.add_task(task)
    assert task in pet.tasks


# ── Scheduler ─────────────────────────────────────────────────────────────────

def test_scheduler_skips_tasks_that_exceed_time():
    owner = Owner(name="Jordan", available_minutes=30)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Walk",  duration_minutes=20, priority="high"),
        Task(title="Bath",  duration_minutes=40, priority="low"),
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan()
    assert len(plan.scheduled_tasks) == 1
    assert plan.skipped_tasks[0].title == "Bath"


def test_scheduler_respects_priority_order():
    owner = Owner(name="Jordan", available_minutes=20)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Play",  duration_minutes=15, priority="low"),
        Task(title="Meds",  duration_minutes=10, priority="high"),
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan()
    assert plan.scheduled_tasks[0].title == "Meds"


# ── Sorting Correctness ────────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_minutes=120)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Evening walk", duration_minutes=20, priority="low",    start_time="18:00"),
        Task(title="Meds",         duration_minutes=10, priority="high",   start_time="08:00"),
        Task(title="Lunch",        duration_minutes=15, priority="medium", start_time="12:00"),
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan(sort_by="time")
    times = [t.start_time for t in plan.scheduled_tasks]
    assert times == sorted(times), f"Expected chronological order, got {times}"


def test_sort_by_time_untimed_tasks_appear_last():
    owner = Owner(name="Jordan", available_minutes=120)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Free play",  duration_minutes=20, priority="low"),
        Task(title="Morning run",duration_minutes=30, priority="high", start_time="07:00"),
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan(sort_by="time")
    assert plan.scheduled_tasks[0].title == "Morning run"
    assert plan.scheduled_tasks[-1].title == "Free play"


# ── Recurrence Logic ───────────────────────────────────────────────────────────

def test_renew_creates_new_incomplete_task():
    task = Task(title="Daily walk", duration_minutes=30, priority="high",
                recurring=True, recurrence="daily")
    task.mark_complete()
    assert task.completed is True

    renewed = task.renew()
    assert renewed.completed is False


def test_renew_preserves_task_attributes():
    task = Task(title="Daily walk", duration_minutes=30, priority="high",
                recurring=True, recurrence="daily", category="walk",
                start_time="08:00")
    task.mark_complete()
    renewed = task.renew()

    assert renewed.title == task.title
    assert renewed.duration_minutes == task.duration_minutes
    assert renewed.priority == task.priority
    assert renewed.recurrence == task.recurrence
    assert renewed.start_time == task.start_time


def test_renew_does_not_mutate_original():
    task = Task(title="Daily walk", duration_minutes=30, recurring=True)
    task.mark_complete()
    task.renew()
    assert task.completed is True  # original unchanged


# ── Conflict Detection ─────────────────────────────────────────────────────────

def test_same_start_time_is_a_conflict():
    owner = Owner(name="Jordan", available_minutes=120)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Walk", duration_minutes=30, priority="high",   start_time="09:00"),
        Task(title="Meds", duration_minutes=15, priority="medium", start_time="09:00"),
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan()
    assert len(plan.conflicts) == 1
    titles = {plan.conflicts[0][0].title, plan.conflicts[0][1].title}
    assert titles == {"Walk", "Meds"}


def test_overlapping_times_are_a_conflict():
    owner = Owner(name="Jordan", available_minutes=120)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Walk", duration_minutes=60, priority="high",   start_time="09:00"),  # 09:00–10:00
        Task(title="Bath", duration_minutes=30, priority="medium", start_time="09:30"),  # 09:30–10:00
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan()
    assert len(plan.conflicts) == 1


def test_adjacent_tasks_are_not_a_conflict():
    owner = Owner(name="Jordan", available_minutes=120)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Walk", duration_minutes=30, priority="high",   start_time="09:00"),  # ends 09:30
        Task(title="Meds", duration_minutes=15, priority="medium", start_time="09:30"),  # starts 09:30
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan()
    assert len(plan.conflicts) == 0


def test_no_conflict_when_only_one_timed_task():
    owner = Owner(name="Jordan", available_minutes=120)
    pet   = Pet(name="Mochi", species="dog", age=3)
    tasks = [
        Task(title="Walk", duration_minutes=30, priority="high", start_time="09:00"),
        Task(title="Play", duration_minutes=20, priority="low"),  # no start_time
    ]
    plan = Scheduler(owner, pet, tasks).generate_plan()
    assert len(plan.conflicts) == 0
