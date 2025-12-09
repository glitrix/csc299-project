"""Tests for task management functionality."""

import pytest
import tempfile
import shutil
from datetime import date, timedelta
from src.studypal.storage import Storage
from src.studypal.tasks import TaskManager


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    temp_dir = tempfile.mkdtemp()
    storage = Storage(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


@pytest.fixture
def task_manager(temp_storage):
    """Create a TaskManager instance for testing."""
    return TaskManager(temp_storage)


def test_add_task(task_manager):
    """Test adding a new task."""
    task_id = task_manager.add_task("Test Task", "Description", priority=3)
    assert task_id == 1
    
    task = task_manager.get_task(task_id)
    assert task is not None
    assert task['title'] == "Test Task"
    assert task['description'] == "Description"
    assert task['priority'] == 3
    assert task['status'] == "todo"


def test_add_task_with_due_date(task_manager):
    """Test adding a task with due date."""
    due_date = "2025-12-31"
    task_id = task_manager.add_task("Test Task", due_date=due_date)
    
    task = task_manager.get_task(task_id)
    assert task['due_date'] == due_date


def test_add_task_invalid_priority(task_manager):
    """Test adding a task with invalid priority."""
    with pytest.raises(ValueError):
        task_manager.add_task("Test Task", priority=10)


def test_get_task(task_manager):
    """Test retrieving a task."""
    task_id = task_manager.add_task("Test Task")
    task = task_manager.get_task(task_id)
    
    assert task is not None
    assert task['id'] == task_id
    assert task['title'] == "Test Task"


def test_list_tasks(task_manager):
    """Test listing all tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.add_task("Task 3")
    
    tasks = task_manager.list_tasks()
    assert len(tasks) == 3


def test_list_tasks_by_status(task_manager):
    """Test listing tasks filtered by status."""
    task_manager.add_task("Task 1", status="todo")
    task_manager.add_task("Task 2", status="in_progress")
    task_manager.add_task("Task 3", status="done")
    
    todo_tasks = task_manager.list_tasks(status="todo")
    assert len(todo_tasks) == 1


def test_list_tasks_by_priority(task_manager):
    """Test listing tasks filtered by priority."""
    task_manager.add_task("Task 1", priority=5)
    task_manager.add_task("Task 2", priority=3)
    task_manager.add_task("Task 3", priority=5)
    
    high_priority = task_manager.list_tasks(priority=5)
    assert len(high_priority) == 2


def test_update_task(task_manager):
    """Test updating a task."""
    task_id = task_manager.add_task("Original Title")
    
    success = task_manager.update_task(task_id, title="Updated Title", priority=4)
    assert success
    
    task = task_manager.get_task(task_id)
    assert task['title'] == "Updated Title"
    assert task['priority'] == 4


def test_mark_complete(task_manager):
    """Test marking a task as complete."""
    task_id = task_manager.add_task("Test Task")
    
    success = task_manager.mark_complete(task_id)
    assert success
    
    task = task_manager.get_task(task_id)
    assert task['status'] == "done"


def test_mark_in_progress(task_manager):
    """Test marking a task as in progress."""
    task_id = task_manager.add_task("Test Task")
    
    success = task_manager.mark_in_progress(task_id)
    assert success
    
    task = task_manager.get_task(task_id)
    assert task['status'] == "in_progress"


def test_delete_task(task_manager):
    """Test deleting a task."""
    task_id = task_manager.add_task("Test Task")
    
    success = task_manager.delete_task(task_id)
    assert success
    
    task = task_manager.get_task(task_id)
    assert task is None


def test_get_tasks_due_soon(task_manager):
    """Test getting tasks due soon."""
    today = date.today()
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (today + timedelta(days=8)).strftime("%Y-%m-%d")
    
    task_manager.add_task("Due Tomorrow", due_date=tomorrow)
    task_manager.add_task("Due Next Week", due_date=next_week)
    
    due_soon = task_manager.get_tasks_due_soon(days=7)
    assert len(due_soon) == 1


def test_get_overdue_tasks(task_manager):
    """Test getting overdue tasks."""
    past_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    future_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    task_manager.add_task("Overdue Task", due_date=past_date)
    task_manager.add_task("Future Task", due_date=future_date)
    
    overdue = task_manager.get_overdue_tasks()
    assert len(overdue) == 1
    assert overdue[0]['title'] == "Overdue Task"


def test_get_statistics(task_manager):
    """Test getting task statistics."""
    task_manager.add_task("Task 1", status="todo")
    task_manager.add_task("Task 2", status="in_progress")
    task_manager.add_task("Task 3", status="done")
    task_manager.add_task("Task 4", status="done")
    
    stats = task_manager.get_statistics()
    assert stats['total'] == 4
    assert stats['todo'] == 1
    assert stats['in_progress'] == 1
    assert stats['done'] == 2
    assert stats['completion_rate'] == 50.0
