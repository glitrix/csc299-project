"""
Task Manager - Main module for managing tasks with JSON storage.
"""
from typing import List, Optional
from datetime import datetime
from task import Task
from storage import JSONStorage


class TaskManager:
    """Main task manager class that handles all task operations."""
    
    def __init__(self, storage_file: str = "tasks.json"):
        """
        Initialize the task manager.
        
        Args:
            storage_file: Path to the JSON file for storing tasks
        """
        self.storage = JSONStorage(storage_file)
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from storage."""
        task_data = self.storage.load_tasks()
        self.tasks = [Task.from_dict(data) for data in task_data]
    
    def save_tasks(self):
        """Save all tasks to storage."""
        task_data = [task.to_dict() for task in self.tasks]
        self.storage.save_tasks(task_data)
    
    def create_task(self, title: str, description: str = "", status: str = "pending") -> Task:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description
            status: Initial status (default: pending)
            
        Returns:
            The created Task object
        """
        task = Task(title=title, description=description, status=status)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self.tasks.copy()
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Get all tasks with a specific status.
        
        Args:
            status: Status to filter by (pending, in-progress, completed)
            
        Returns:
            List of tasks matching the status
        """
        return [task for task in self.tasks if task.status == status]
    
    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> bool:
        """
        Update a task's properties.
        
        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            status: New status (optional)
            
        Returns:
            True if task was updated, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        
        task.update_timestamp()
        self.save_tasks()
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description.
        
        Args:
            query: Search query string
            
        Returns:
            List of tasks matching the query
        """
        query_lower = query.lower()
        return [
            task for task in self.tasks
            if query_lower in task.title.lower() or query_lower in task.description.lower()
        ]
    
    def clear_completed_tasks(self) -> int:
        """
        Remove all completed tasks.
        
        Returns:
            Number of tasks removed
        """
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.status != "completed"]
        removed_count = initial_count - len(self.tasks)
        if removed_count > 0:
            self.save_tasks()
        return removed_count
    
    def get_statistics(self) -> dict:
        """
        Get statistics about tasks.
        
        Returns:
            Dictionary with task statistics
        """
        total = len(self.tasks)
        pending = len(self.get_tasks_by_status("pending"))
        in_progress = len(self.get_tasks_by_status("in-progress"))
        completed = len(self.get_tasks_by_status("completed"))
        
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed
        }
