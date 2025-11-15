"""
JSON storage handler for persisting tasks.
"""
import json
import os
from typing import List, Dict, Any
from pathlib import Path


class JSONStorage:
    """Handles reading and writing tasks to JSON files."""
    
    def __init__(self, filepath: str = "tasks.json"):
        """
        Initialize the storage handler.
        
        Args:
            filepath: Path to the JSON file for storing tasks
        """
        self.filepath = Path(filepath)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the JSON file if it doesn't exist."""
        if not self.filepath.exists():
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self._write_data([])
    
    def _read_data(self) -> List[Dict[str, Any]]:
        """
        Read data from the JSON file.
        
        Returns:
            List of task dictionaries
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {self.filepath}. Starting with empty data.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    def _write_data(self, data: List[Dict[str, Any]]):
        """
        Write data to the JSON file.
        
        Args:
            data: List of task dictionaries to write
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing to file: {e}")
            raise
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """
        Load all tasks from the JSON file.
        
        Returns:
            List of task dictionaries
        """
        return self._read_data()
    
    def save_tasks(self, tasks: List[Dict[str, Any]]):
        """
        Save all tasks to the JSON file.
        
        Args:
            tasks: List of task dictionaries to save
        """
        self._write_data(tasks)
    
    def backup(self, backup_path: str = None):
        """
        Create a backup of the current tasks file.
        
        Args:
            backup_path: Optional custom backup path
        """
        if backup_path is None:
            backup_path = str(self.filepath) + ".backup"
        
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
                print(f"Backup created at {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
