"""Storage module for StudyPal - handles JSON file operations."""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class Storage:
    """Handles reading and writing data to JSON files."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize storage with data directory path.
        
        Args:
            data_dir: Path to directory containing JSON data files
        """
        self.data_dir = Path(data_dir)
        self.notes_file = self.data_dir / "notes.json"
        self.tasks_file = self.data_dir / "tasks.json"
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize files if they don't exist
        self._init_file(self.notes_file, {"notes": [], "links": [], "next_id": 1})
        self._init_file(self.tasks_file, {"tasks": [], "next_id": 1})
    
    def _init_file(self, filepath: Path, default_data: Dict) -> None:
        """Initialize a JSON file with default data if it doesn't exist.
        
        Args:
            filepath: Path to the JSON file
            default_data: Default data structure to initialize with
        """
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=2)
    
    def _read_json(self, filepath: Path) -> Dict:
        """Read and parse a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Dictionary containing the parsed JSON data
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {filepath}: {e}")
            return {}
    
    def _write_json(self, filepath: Path, data: Dict) -> None:
        """Write data to a JSON file.
        
        Args:
            filepath: Path to the JSON file
            data: Dictionary to write as JSON
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
    
    # Notes operations
    def load_notes(self) -> Dict:
        """Load all notes data from JSON file.
        
        Returns:
            Dictionary containing notes, links, and next_id
        """
        return self._read_json(self.notes_file)
    
    def save_notes(self, data: Dict) -> None:
        """Save notes data to JSON file.
        
        Args:
            data: Dictionary containing notes, links, and next_id
        """
        self._write_json(self.notes_file, data)
    
    def add_note(self, note: Dict) -> int:
        """Add a new note to storage.
        
        Args:
            note: Dictionary containing note data
            
        Returns:
            ID of the newly created note
        """
        data = self.load_notes()
        note_id = data['next_id']
        note['id'] = note_id
        note['created_at'] = datetime.now().isoformat()
        note['updated_at'] = datetime.now().isoformat()
        data['notes'].append(note)
        data['next_id'] += 1
        self.save_notes(data)
        return note_id
    
    def get_note(self, note_id: int) -> Dict | None:
        """Retrieve a note by ID.
        
        Args:
            note_id: ID of the note to retrieve
            
        Returns:
            Note dictionary if found, None otherwise
        """
        data = self.load_notes()
        for note in data['notes']:
            if note['id'] == note_id:
                return note
        return None
    
    def update_note(self, note_id: int, updates: Dict) -> bool:
        """Update an existing note.
        
        Args:
            note_id: ID of the note to update
            updates: Dictionary of fields to update
            
        Returns:
            True if note was updated, False if not found
        """
        data = self.load_notes()
        for note in data['notes']:
            if note['id'] == note_id:
                note.update(updates)
                note['updated_at'] = datetime.now().isoformat()
                self.save_notes(data)
                return True
        return False
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID.
        
        Args:
            note_id: ID of the note to delete
            
        Returns:
            True if note was deleted, False if not found
        """
        data = self.load_notes()
        original_len = len(data['notes'])
        data['notes'] = [n for n in data['notes'] if n['id'] != note_id]
        if len(data['notes']) < original_len:
            self.save_notes(data)
            return True
        return False
    
    def add_link(self, from_id: int, to_id: int, link_type: str = "related") -> None:
        """Add a link between two notes.
        
        Args:
            from_id: ID of the source note
            to_id: ID of the target note
            link_type: Type of link (default: "related")
        """
        data = self.load_notes()
        link = {
            "from_note_id": from_id,
            "to_note_id": to_id,
            "link_type": link_type
        }
        data['links'].append(link)
        self.save_notes(data)
    
    def get_links(self, note_id: int) -> List[Dict]:
        """Get all links for a note.
        
        Args:
            note_id: ID of the note
            
        Returns:
            List of link dictionaries
        """
        data = self.load_notes()
        return [link for link in data['links'] 
                if link['from_note_id'] == note_id or link['to_note_id'] == note_id]
    
    # Tasks operations
    def load_tasks(self) -> Dict:
        """Load all tasks data from JSON file.
        
        Returns:
            Dictionary containing tasks and next_id
        """
        return self._read_json(self.tasks_file)
    
    def save_tasks(self, data: Dict) -> None:
        """Save tasks data to JSON file.
        
        Args:
            data: Dictionary containing tasks and next_id
        """
        self._write_json(self.tasks_file, data)
    
    def add_task(self, task: Dict) -> int:
        """Add a new task to storage.
        
        Args:
            task: Dictionary containing task data
            
        Returns:
            ID of the newly created task
        """
        data = self.load_tasks()
        task_id = data['next_id']
        task['id'] = task_id
        task['created_at'] = datetime.now().isoformat()
        task['updated_at'] = datetime.now().isoformat()
        data['tasks'].append(task)
        data['next_id'] += 1
        self.save_tasks(data)
        return task_id
    
    def get_task(self, task_id: int) -> Dict | None:
        """Retrieve a task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task dictionary if found, None otherwise
        """
        data = self.load_tasks()
        for task in data['tasks']:
            if task['id'] == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, updates: Dict) -> bool:
        """Update an existing task.
        
        Args:
            task_id: ID of the task to update
            updates: Dictionary of fields to update
            
        Returns:
            True if task was updated, False if not found
        """
        data = self.load_tasks()
        for task in data['tasks']:
            if task['id'] == task_id:
                task.update(updates)
                task['updated_at'] = datetime.now().isoformat()
                self.save_tasks(data)
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False if not found
        """
        data = self.load_tasks()
        original_len = len(data['tasks'])
        data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
        if len(data['tasks']) < original_len:
            self.save_tasks(data)
            return True
        return False
