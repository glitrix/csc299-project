"""Task management module for StudyPal."""

from typing import List, Dict, Optional
from datetime import datetime, date
from .storage import Storage
from .utils import validate_priority, validate_status


class TaskManager:
    """Task management system for tracking tasks and deadlines."""
    
    def __init__(self, storage: Storage):
        """Initialize TaskManager with a storage backend.
        
        Args:
            storage: Storage instance for data persistence
        """
        self.storage = storage
    
    def add_task(self, title: str, description: str = "", 
                 priority: int = 2, due_date: Optional[str] = None,
                 status: str = "todo") -> int:
        """Create a new task.
        
        Args:
            title: Title of the task
            description: Detailed description
            priority: Priority level (1-5, where 5 is highest)
            due_date: Due date in YYYY-MM-DD format
            status: Initial status (todo, in_progress, done)
            
        Returns:
            ID of the newly created task
        """
        if not validate_priority(priority):
            raise ValueError("Priority must be between 1 and 5")
        
        if not validate_status(status):
            raise ValueError("Status must be one of: todo, in_progress, done")
        
        task = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date
        }
        return self.storage.add_task(task)
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Retrieve a task by ID.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task dictionary if found, None otherwise
        """
        return self.storage.get_task(task_id)
    
    def list_tasks(self, status: Optional[str] = None, 
                   priority: Optional[int] = None) -> List[Dict]:
        """List all tasks, optionally filtered by status or priority.
        
        Args:
            status: Optional status to filter by
            priority: Optional priority to filter by
            
        Returns:
            List of task dictionaries
        """
        data = self.storage.load_tasks()
        tasks = data['tasks']
        
        if status:
            tasks = [t for t in tasks if t['status'] == status]
        
        if priority is not None:
            tasks = [t for t in tasks if t['priority'] == priority]
        
        return tasks
    
    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, status: Optional[str] = None,
                    priority: Optional[int] = None, due_date: Optional[str] = None) -> bool:
        """Update an existing task.
        
        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            status: New status (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
            
        Returns:
            True if task was updated, False if not found
        """
        updates = {}
        
        if title is not None:
            updates['title'] = title
        if description is not None:
            updates['description'] = description
        if status is not None:
            if not validate_status(status):
                raise ValueError("Status must be one of: todo, in_progress, done")
            updates['status'] = status
        if priority is not None:
            if not validate_priority(priority):
                raise ValueError("Priority must be between 1 and 5")
            updates['priority'] = priority
        if due_date is not None:
            updates['due_date'] = due_date
        
        return self.storage.update_task(task_id, updates)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False if not found
        """
        return self.storage.delete_task(task_id)
    
    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as completed.
        
        Args:
            task_id: ID of the task
            
        Returns:
            True if task was updated, False if not found
        """
        return self.update_task(task_id, status="done")
    
    def mark_in_progress(self, task_id: int) -> bool:
        """Mark a task as in progress.
        
        Args:
            task_id: ID of the task
            
        Returns:
            True if task was updated, False if not found
        """
        return self.update_task(task_id, status="in_progress")
    
    def get_tasks_due_soon(self, days: int = 7) -> List[Dict]:
        """Get tasks due within a specified number of days.
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of task dictionaries due within the timeframe
        """
        data = self.storage.load_tasks()
        today = date.today()
        due_soon = []
        
        for task in data['tasks']:
            if task['status'] == 'done':
                continue
            
            due_date_str = task.get('due_date')
            if not due_date_str:
                continue
            
            try:
                task_due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                days_until = (task_due_date - today).days
                
                if 0 <= days_until <= days:
                    due_soon.append(task)
            except ValueError:
                # Skip tasks with invalid date format
                continue
        
        # Sort by due date
        due_soon.sort(key=lambda t: t['due_date'])
        return due_soon
    
    def get_overdue_tasks(self) -> List[Dict]:
        """Get all tasks that are past their due date.
        
        Returns:
            List of overdue task dictionaries
        """
        data = self.storage.load_tasks()
        today = date.today()
        overdue = []
        
        for task in data['tasks']:
            if task['status'] == 'done':
                continue
            
            due_date_str = task.get('due_date')
            if not due_date_str:
                continue
            
            try:
                task_due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                
                if task_due_date < today:
                    overdue.append(task)
            except ValueError:
                continue
        
        # Sort by due date
        overdue.sort(key=lambda t: t['due_date'])
        return overdue
    
    def get_tasks_by_priority(self, priority: int) -> List[Dict]:
        """Get all tasks with a specific priority level.
        
        Args:
            priority: Priority level (1-5)
            
        Returns:
            List of task dictionaries with the specified priority
        """
        return self.list_tasks(priority=priority)
    
    def get_statistics(self) -> Dict:
        """Get statistics about tasks.
        
        Returns:
            Dictionary containing task statistics
        """
        data = self.storage.load_tasks()
        tasks = data['tasks']
        
        total = len(tasks)
        todo = len([t for t in tasks if t['status'] == 'todo'])
        in_progress = len([t for t in tasks if t['status'] == 'in_progress'])
        done = len([t for t in tasks if t['status'] == 'done'])
        
        overdue = len(self.get_overdue_tasks())
        due_soon = len(self.get_tasks_due_soon(7))
        
        return {
            "total": total,
            "todo": todo,
            "in_progress": in_progress,
            "done": done,
            "overdue": overdue,
            "due_this_week": due_soon,
            "completion_rate": (done / total * 100) if total > 0 else 0
        }
