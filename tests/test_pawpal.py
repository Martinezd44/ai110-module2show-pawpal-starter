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
