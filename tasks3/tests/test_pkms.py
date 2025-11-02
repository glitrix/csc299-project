import pytest
import tempfile
import shutil
from pathlib import Path
from tasks3.pkms import PKMSCore


class TestPKMSCore:
    """Test cases for PKMSCore functionality."""
    
    @pytest.fixture
    def temp_pkms(self):
        """Create a temporary PKMS instance for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        pkms = PKMSCore(data_dir=temp_dir)
        yield pkms
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_add_task_valid(self, temp_pkms):
        """Test adding a valid task."""
        task = temp_pkms.add_task("Test Task", "Test description", "high")
        
        assert task['id'] == 1
        assert task['title'] == "Test Task"
        assert task['description'] == "Test description"
        assert task['priority'] == "high"
        assert task['status'] == "pending"
        assert task['completed'] is False
        assert 'created_at' in task
        assert 'updated_at' in task
    
    def test_add_task_invalid_priority(self, temp_pkms):
        """Test adding task with invalid priority raises error."""
        with pytest.raises(ValueError, match="Invalid priority"):
            temp_pkms.add_task("Test Task", "", "invalid_priority")
    
    def test_add_task_empty_title(self, temp_pkms):
        """Test adding task with empty title raises error."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            temp_pkms.add_task("", "Description")
        
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            temp_pkms.add_task("   ", "Description")
    
    def test_complete_task(self, temp_pkms):
        """Test completing a task."""
        task = temp_pkms.add_task("Test Task")
        task_id = task['id']
        
        # Complete the task
        result = temp_pkms.complete_task(task_id)
        assert result is True
        
        # Verify task is completed
        completed_task = temp_pkms.get_task_by_id(task_id)
        assert completed_task['status'] == 'completed'
        assert completed_task['completed'] is True
    
    def test_complete_nonexistent_task(self, temp_pkms):
        """Test completing a non-existent task returns False."""
        result = temp_pkms.complete_task(999)
        assert result is False
    
    def test_delete_task(self, temp_pkms):
        """Test deleting a task."""
        task = temp_pkms.add_task("Test Task")
        task_id = task['id']
        
        # Verify task exists
        assert temp_pkms.get_task_by_id(task_id) is not None
        
        # Delete the task
        result = temp_pkms.delete_task(task_id)
        assert result is True
        
        # Verify task is deleted
        assert temp_pkms.get_task_by_id(task_id) is None
    
    def test_delete_nonexistent_task(self, temp_pkms):
        """Test deleting a non-existent task returns False."""
        result = temp_pkms.delete_task(999)
        assert result is False
    
    def test_list_tasks_all(self, temp_pkms):
        """Test listing all tasks."""
        temp_pkms.add_task("Task 1", "", "high")
        temp_pkms.add_task("Task 2", "", "medium")
        temp_pkms.add_task("Task 3", "", "low")
        
        tasks = temp_pkms.list_tasks()
        assert len(tasks) == 3
        assert all(task['status'] == 'pending' for task in tasks)
    
    def test_list_tasks_by_status(self, temp_pkms):
        """Test listing tasks filtered by status."""
        task1 = temp_pkms.add_task("Task 1")
        task2 = temp_pkms.add_task("Task 2")
        
        # Complete one task
        temp_pkms.complete_task(task1['id'])
        
        # Test pending tasks
        pending_tasks = temp_pkms.list_tasks("pending")
        assert len(pending_tasks) == 1
        assert pending_tasks[0]['id'] == task2['id']
        
        # Test completed tasks
        completed_tasks = temp_pkms.list_tasks("completed")
        assert len(completed_tasks) == 1
        assert completed_tasks[0]['id'] == task1['id']
    
    def test_add_note_valid(self, temp_pkms):
        """Test adding a valid note."""
        note = temp_pkms.add_note("Test Note", "Test content")
        
        assert note['id'] == 1
        assert note['title'] == "Test Note"
        assert note['content'] == "Test content"
        assert 'created_at' in note
        assert 'updated_at' in note
    
    def test_add_note_empty_title(self, temp_pkms):
        """Test adding note with empty title raises error."""
        with pytest.raises(ValueError, match="Note title cannot be empty"):
            temp_pkms.add_note("", "Content")
        
        with pytest.raises(ValueError, match="Note title cannot be empty"):
            temp_pkms.add_note("   ", "Content")
    
    def test_search_tasks(self, temp_pkms):
        """Test searching tasks by keyword."""
        temp_pkms.add_task("Python Development", "Work on Python project")
        temp_pkms.add_task("JavaScript Learning", "Learn JS frameworks")
        temp_pkms.add_task("Database Design", "Design database schema")
        
        # Search by title
        python_tasks = temp_pkms.search_tasks("python")
        assert len(python_tasks) == 1
        assert python_tasks[0]['title'] == "Python Development"
        
        # Search by description
        project_tasks = temp_pkms.search_tasks("project")
        assert len(project_tasks) == 1
        assert project_tasks[0]['title'] == "Python Development"
        
        # Search with no matches
        no_matches = temp_pkms.search_tasks("nonexistent")
        assert len(no_matches) == 0
    
    def test_task_stats(self, temp_pkms):
        """Test getting task statistics."""
        # Add various tasks
        task1 = temp_pkms.add_task("Task 1", "", "high")
        task2 = temp_pkms.add_task("Task 2", "", "high")
        task3 = temp_pkms.add_task("Task 3", "", "medium")
        
        # Complete one task
        temp_pkms.complete_task(task1['id'])
        
        stats = temp_pkms.get_task_stats()
        
        assert stats['total'] == 3
        assert stats['pending'] == 2
        assert stats['completed'] == 1
        assert stats['high_priority'] == 2
    
    def test_generate_id_increments(self, temp_pkms):
        """Test that IDs are generated incrementally."""
        task1 = temp_pkms.add_task("Task 1")
        task2 = temp_pkms.add_task("Task 2")
        task3 = temp_pkms.add_task("Task 3")
        
        assert task1['id'] == 1
        assert task2['id'] == 2
        assert task3['id'] == 3
    
    def test_data_persistence(self, temp_pkms):
        """Test that data persists across PKMS instances."""
        # Add data to first instance
        temp_pkms.add_task("Persistent Task")
        temp_pkms.add_note("Persistent Note")
        
        # Create new instance with same data directory
        new_pkms = PKMSCore(data_dir=temp_pkms.data_dir)
        
        # Verify data is loaded
        tasks = new_pkms.list_tasks()
        notes = new_pkms.list_notes()
        
        assert len(tasks) == 1
        assert len(notes) == 1
        assert tasks[0]['title'] == "Persistent Task"
        assert notes[0]['title'] == "Persistent Note"