"""
Task class definition for the task manager.
"""
from datetime import datetime
from typing import Optional


class Task:
    """Represents a single task with all its properties."""
    
    def __init__(
        self,
        title: str,
        description: str = "",
        status: str = "pending",
        task_id: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        """
        Initialize a new task.
        
        Args:
            title: The title of the task
            description: Detailed description of the task
            status: Current status (pending, in-progress, completed)
            task_id: Unique identifier for the task
            created_at: Timestamp when task was created
            updated_at: Timestamp when task was last updated
        """
        self.id = task_id or self._generate_id()
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    @staticmethod
    def _generate_id() -> str:
        """Generate a unique ID based on timestamp."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary."""
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            task_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def update_timestamp(self):
        """Update the last modified timestamp."""
        self.updated_at = datetime.now().isoformat()
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"[{self.status.upper()}] {self.title}"
