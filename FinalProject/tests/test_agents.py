"""Tests for AI agents."""

import pytest
import tempfile
import shutil
from src.studypal.storage import Storage
from src.studypal.pkms import PKMS
from src.studypal.tasks import TaskManager
from src.studypal.agents import LinkSuggester, TagSuggester, StudyPlanner, SummaryGenerator


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    temp_dir = tempfile.mkdtemp()
    storage = Storage(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


@pytest.fixture
def pkms(temp_storage):
    """Create a PKMS instance for testing."""
    return PKMS(temp_storage)


@pytest.fixture
def task_manager(temp_storage):
    """Create a TaskManager instance for testing."""
    return TaskManager(temp_storage)


@pytest.fixture
def link_suggester(pkms):
    """Create a LinkSuggester instance."""
    return LinkSuggester(pkms)


@pytest.fixture
def tag_suggester(pkms):
    """Create a TagSuggester instance."""
    return TagSuggester(pkms)


@pytest.fixture
def study_planner(task_manager, pkms):
    """Create a StudyPlanner instance."""
    return StudyPlanner(task_manager, pkms)


@pytest.fixture
def summary_generator(pkms):
    """Create a SummaryGenerator instance."""
    return SummaryGenerator(pkms)


def test_link_suggester_basic(pkms, link_suggester):
    """Test basic link suggestion."""
    note1_id = pkms.add_note("Python Basics", "Learn Python programming fundamentals")
    note2_id = pkms.add_note("Python Advanced", "Advanced Python programming techniques")
    note3_id = pkms.add_note("Java Tutorial", "Learn Java programming")
    
    suggestions = link_suggester.suggest_links(note1_id)
    
    # Should suggest note2 (Python Advanced) due to similar content
    assert len(suggestions) > 0
    suggested_ids = [s['note']['id'] for s in suggestions]
    assert note2_id in suggested_ids


def test_link_suggester_with_tags(pkms, link_suggester):
    """Test link suggestion with tag similarity."""
    note1_id = pkms.add_note("Python Basics", "Python intro", tags=["python", "programming"])
    note2_id = pkms.add_note("Advanced Python", "Advanced concepts", tags=["python", "advanced"])
    note3_id = pkms.add_note("Java Basics", "Java intro", tags=["java"])
    
    suggestions = link_suggester.suggest_links(note1_id)
    
    # Should suggest note2 due to shared "python" tag
    assert len(suggestions) > 0
    suggested_ids = [s['note']['id'] for s in suggestions]
    assert note2_id in suggested_ids


def test_link_suggester_excludes_existing_links(pkms, link_suggester):
    """Test that already linked notes are not suggested."""
    note1_id = pkms.add_note("Note 1", "Python programming")
    note2_id = pkms.add_note("Note 2", "Python programming")
    
    # Link them first
    pkms.link_notes(note1_id, note2_id)
    
    # Should not suggest note2 since it's already linked
    suggestions = link_suggester.suggest_links(note1_id)
    suggested_ids = [s['note']['id'] for s in suggestions]
    assert note2_id not in suggested_ids


def test_tag_suggester(pkms, tag_suggester):
    """Test tag suggestion."""
    # Create notes with existing tags
    pkms.add_note("Python Tutorial", "Learn Python", tags=["python", "programming"])
    pkms.add_note("Java Guide", "Learn Java", tags=["java", "programming"])
    
    # Create a new note without tags that mentions python
    note_id = pkms.add_note("New Python Note", "This is about python programming")
    
    suggestions = tag_suggester.suggest_tags(note_id)
    
    # Should suggest "python" and "programming" based on content
    assert "python" in suggestions or "programming" in suggestions


def test_study_planner_plan_week(task_manager, pkms, study_planner):
    """Test weekly study plan generation."""
    # Add some tasks
    task_manager.add_task("Task 1", priority=5, due_date="2025-11-20")
    task_manager.add_task("Task 2", priority=3, due_date="2025-11-25")
    
    plan = study_planner.plan_week()
    
    # Should return a dict with days of the week
    assert len(plan) == 7
    assert "Monday" in plan
    assert "Sunday" in plan


def test_study_planner_daily_schedule(task_manager, pkms, study_planner):
    """Test daily schedule suggestion."""
    from datetime import date, timedelta
    
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Add tasks with different priorities and due dates
    task_manager.add_task("High Priority", priority=5)
    task_manager.add_task("Due Soon", priority=3, due_date=tomorrow)
    task_manager.add_task("Low Priority", priority=1)
    
    schedule = study_planner.suggest_daily_schedule()
    
    # Should return tasks, prioritizing high priority and due soon
    assert len(schedule) > 0
    assert schedule[0]['priority'] >= 3 or schedule[0].get('due_date') == tomorrow


def test_summary_generator(pkms, summary_generator):
    """Test summary generation."""
    content = """This is the first sentence. This is the second sentence. 
                 This is the third sentence. This is the fourth sentence."""
    note_id = pkms.add_note("Test Note", content)
    
    summary = summary_generator.generate_summary(note_id, max_sentences=2)
    
    # Summary should be shorter than original content
    assert len(summary) < len(content)
    assert summary != ""


def test_summary_generator_short_content(pkms, summary_generator):
    """Test summary with short content."""
    content = "Short content."
    note_id = pkms.add_note("Test Note", content)
    
    summary = summary_generator.generate_summary(note_id)
    
    # For short content, should return the full content
    assert summary == content


def test_summary_generator_no_content(pkms, summary_generator):
    """Test summary with no content."""
    note_id = pkms.add_note("Empty Note", "")
    
    summary = summary_generator.generate_summary(note_id)
    
    # Should return a message indicating no content
    assert "no content" in summary.lower()


def test_summarize_all_notes(pkms, summary_generator):
    """Test summarizing all notes."""
    pkms.add_note("Note 1", "Content for note 1", tags=["test"])
    pkms.add_note("Note 2", "Content for note 2", tags=["test"])
    pkms.add_note("Note 3", "Content for note 3", tags=["other"])
    
    # Summarize all notes with "test" tag
    summaries = summary_generator.summarize_all_notes(tag="test")
    
    assert len(summaries) == 2
    assert all('summary' in s for s in summaries)
