#!/usr/bin/env python3
"""
Personal Knowledge Management System (PKMS) - Tasks3 Version

A simplified version of the PKMS for tasks3 package with testing support.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Any, Optional


# Configuration
DATA_DIR = Path(__file__).parent / "data"
TASKS_FILE = DATA_DIR / "tasks.json"
NOTES_FILE = DATA_DIR / "notes.json"


class PKMSCore:
    """Core PKMS functionality for tasks3."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize PKMS with optional custom data directory."""
        if data_dir:
            self.data_dir = data_dir
            self.tasks_file = data_dir / "tasks.json"
            self.notes_file = data_dir / "notes.json"
        else:
            self.data_dir = DATA_DIR
            self.tasks_file = TASKS_FILE
            self.notes_file = NOTES_FILE
        
        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        self.tasks = self.load_data(self.tasks_file, [])
        self.notes = self.load_data(self.notes_file, [])
    
    def load_data(self, file_path: Path, default: Any) -> Any:
        """Load data from JSON file with error handling."""
        if not file_path.exists():
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default
    
    def save_data(self, data: Any, file_path: Path) -> None:
        """Save data to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def save_all(self) -> None:
        """Save all data files."""
        self.save_data(self.tasks, self.tasks_file)
        self.save_data(self.notes, self.notes_file)
    
    def generate_id(self, items: List[Dict[str, Any]]) -> int:
        """Generate a new ID for items."""
        if not items:
            return 1
        return max(item.get('id', 0) for item in items) + 1
    
    def get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Dict[str, Any]:
        """Add a new task."""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError(f"Invalid priority: {priority}")
        
        new_task = {
            'id': self.generate_id(self.tasks),
            'title': title.strip(),
            'description': description.strip(),
            'priority': priority,
            'status': 'pending',
            'completed': False,
            'created_at': self.get_timestamp(),
            'updated_at': self.get_timestamp()
        }
        
        self.tasks.append(new_task)
        self.save_data(self.tasks, self.tasks_file)
        
        return new_task
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get task by ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        task['status'] = 'completed'
        task['completed'] = True
        task['updated_at'] = self.get_timestamp()
        
        self.save_data(self.tasks, self.tasks_file)
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(i)
                self.save_data(self.tasks, self.tasks_file)
                return True
        return False
    
    def list_tasks(self, status: str = "all") -> List[Dict[str, Any]]:
        """List tasks with optional status filter."""
        if status == "all":
            return self.tasks.copy()
        else:
            return [task for task in self.tasks if task['status'] == status]
    
    def add_note(self, title: str, content: str = "") -> Dict[str, Any]:
        """Add a new note."""
        if not title.strip():
            raise ValueError("Note title cannot be empty")
        
        new_note = {
            'id': self.generate_id(self.notes),
            'title': title.strip(),
            'content': content.strip(),
            'created_at': self.get_timestamp(),
            'updated_at': self.get_timestamp()
        }
        
        self.notes.append(new_note)
        self.save_data(self.notes, self.notes_file)
        
        return new_note
    
    def get_note_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        """Get note by ID."""
        for note in self.notes:
            if note['id'] == note_id:
                return note
        return None
    
    def list_notes(self) -> List[Dict[str, Any]]:
        """List all notes."""
        return self.notes.copy()
    
    def search_tasks(self, keyword: str) -> List[Dict[str, Any]]:
        """Search tasks by keyword in title or description."""
        keyword = keyword.lower()
        results = []
        
        for task in self.tasks:
            if (keyword in task['title'].lower() or 
                keyword in task.get('description', '').lower()):
                results.append(task)
        
        return results
    
    def get_task_stats(self) -> Dict[str, int]:
        """Get task statistics."""
        stats = {
            'total': len(self.tasks),
            'pending': 0,
            'completed': 0,
            'high_priority': 0
        }
        
        for task in self.tasks:
            if task['status'] == 'pending':
                stats['pending'] += 1
            elif task['status'] == 'completed':
                stats['completed'] += 1
            
            if task['priority'] == 'high':
                stats['high_priority'] += 1
        
        return stats


def create_sample_data(pkms: PKMSCore) -> None:
    """Create some sample data for demonstration."""
    # Add sample tasks
    pkms.add_task("Complete project documentation", "Write comprehensive docs", "high")
    pkms.add_task("Review code", "Review pull requests", "medium")
    pkms.add_task("Update dependencies", "Update to latest versions", "low")
    
    # Add sample notes
    pkms.add_note("Meeting Notes", "Discussed project timeline and deliverables")
    pkms.add_note("Ideas", "New feature ideas for next sprint")


def run_demo() -> None:
    """Run a demonstration of PKMS functionality."""
    print("=== PKMS Tasks3 Demo ===")
    
    # Create PKMS instance
    pkms = PKMSCore()
    
    # Create sample data
    create_sample_data(pkms)
    
    # Display tasks
    print("\nCurrent Tasks:")
    for task in pkms.list_tasks():
        status_icon = "✓" if task['completed'] else "○"
        print(f"  {status_icon} ID:{task['id']} [{task['priority']}] {task['title']}")
    
    # Display notes
    print("\nCurrent Notes:")
    for note in pkms.list_notes():
        print(f"  • ID:{note['id']} {note['title']}")
    
    # Show stats
    stats = pkms.get_task_stats()
    print(f"\nTask Statistics:")
    print(f"  Total: {stats['total']}")
    print(f"  Pending: {stats['pending']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  High Priority: {stats['high_priority']}")


if __name__ == "__main__":
    run_demo()