"""Tests for OpenAI integration in agents module."""

import os
import pytest
from studypal.storage import Storage
from studypal.pkms import PKMS
from studypal.tasks import TaskManager
from studypal.agents import StudyPlanner

# Skip all tests in this file if no valid API key
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "").startswith("sk-test"),
    reason="OpenAI tests require a valid API key"
)


@pytest.fixture
def setup_with_tasks(tmp_path):
    """Setup with some test tasks."""
    storage = Storage(str(tmp_path))
    pkms = PKMS(storage)
    task_manager = TaskManager(storage)
    
    # Add some test tasks
    task_manager.add_task("Complete Python assignment", priority=5, due_date="2025-11-15")
    task_manager.add_task("Study algorithms", priority=4, due_date="2025-11-18")
    task_manager.add_task("Review notes", priority=3)
    
    return task_manager, pkms


def test_planner_works_without_api_key(setup_with_tasks):
    """Test that planner works in basic mode without API key."""
    task_manager, pkms = setup_with_tasks
    planner = StudyPlanner(task_manager, pkms)
    
    # Should work without API key
    plan = planner.plan_week()
    assert isinstance(plan, dict)
    assert len(plan) == 7  # 7 days
    
    # Should have some tasks scheduled
    total_activities = sum(len(activities) for activities in plan.values())
    assert total_activities > 0


def test_planner_with_api_key(setup_with_tasks):
    """Test planner with OpenAI API key if configured."""
    task_manager, pkms = setup_with_tasks
    planner = StudyPlanner(task_manager, pkms)
    
    if not planner.openai_client:
        pytest.skip("OpenAI API key not configured - skipping AI test")
    
    # Test weekly plan
    plan = planner.plan_week()
    assert isinstance(plan, dict)
    assert len(plan) == 7
    
    # Should have tasks scheduled
    total_activities = sum(len(activities) for activities in plan.values())
    assert total_activities > 0


def test_daily_schedule_without_api_key(setup_with_tasks):
    """Test daily schedule works without API key."""
    task_manager, pkms = setup_with_tasks
    planner = StudyPlanner(task_manager, pkms)
    
    # Should work without API key
    daily = planner.suggest_daily_schedule()
    assert isinstance(daily, list)
    assert len(daily) <= 5  # Max 5 tasks


def test_daily_schedule_with_api_key(setup_with_tasks):
    """Test daily schedule with OpenAI API key if configured."""
    task_manager, pkms = setup_with_tasks
    planner = StudyPlanner(task_manager, pkms)
    
    if not planner.openai_client:
        pytest.skip("OpenAI API key not configured - skipping AI test")
    
    daily = planner.suggest_daily_schedule()
    assert isinstance(daily, list)
    assert len(daily) <= 5


def test_openai_fallback_on_error(setup_with_tasks, monkeypatch):
    """Test that system falls back to basic planning on API error."""
    task_manager, pkms = setup_with_tasks
    planner = StudyPlanner(task_manager, pkms)
    
    if not planner.openai_client:
        pytest.skip("OpenAI API key not configured - skipping fallback test")
    
    # Mock the AI method to raise an exception
    def mock_ai_error(*args, **kwargs):
        raise Exception("API Error")
    
    monkeypatch.setattr(planner, "_plan_week_with_ai", mock_ai_error)
    
    # Should fall back to basic planning
    plan = planner.plan_week()
    assert isinstance(plan, dict)
    assert len(plan) == 7
