#!/usr/bin/env python3
"""
Personal Knowledge Management System (PKMS) - Enhanced Task Manager

An advanced command-line application for managing tasks, notes, and knowledge items
with enhanced features for personal knowledge management.

Features:
- Task management with priorities and due dates
- Note-taking and knowledge storage
- Tagging system for organization
- Categories and projects
- Advanced search and filtering
- Import/export capabilities
- Task dependencies and relationships

Usage:
    python pkms.py task add "Task title" --description "desc" --priority high --due 2025-11-10
    python pkms.py task list --status pending --priority high
    python pkms.py note add "Note title" --content "Note content" --tags "python,learning"
    python pkms.py search "keyword" --type all
    python pkms.py export --format json
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Set
import re


# Configuration
DATA_DIR = Path(__file__).parent / "data"
TASKS_FILE = DATA_DIR / "tasks.json"
NOTES_FILE = DATA_DIR / "notes.json"
CONFIG_FILE = DATA_DIR / "config.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


class PKMSManager:
    """Main class for Personal Knowledge Management System."""
    
    def __init__(self):
        self.tasks = self.load_data(TASKS_FILE, [])
        self.notes = self.load_data(NOTES_FILE, [])
        self.config = self.load_data(CONFIG_FILE, self.default_config())
    
    def default_config(self) -> Dict[str, Any]:
        """Default configuration settings."""
        return {
            "priorities": ["low", "medium", "high", "urgent"],
            "categories": ["personal", "work", "learning", "project"],
            "date_format": "%Y-%m-%d",
            "datetime_format": "%Y-%m-%d %H:%M:%S"
        }
    
    def load_data(self, file_path: Path, default: Any) -> Any:
        """Load data from JSON file with error handling."""
        if not file_path.exists():
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not read {file_path.name}. Using default data.")
            return default
    
    def save_data(self, data: Any, file_path: Path) -> None:
        """Save data to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def save_all(self) -> None:
        """Save all data files."""
        self.save_data(self.tasks, TASKS_FILE)
        self.save_data(self.notes, NOTES_FILE)
        self.save_data(self.config, CONFIG_FILE)
    
    def generate_id(self, items: List[Dict[str, Any]]) -> int:
        """Generate a new ID for items."""
        if not items:
            return 1
        return max(item.get('id', 0) for item in items) + 1
    
    def get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime(self.config["datetime_format"])
    
    def parse_date(self, date_str: str) -> Optional[str]:
        """Parse date string and return formatted date."""
        if not date_str:
            return None
        
        try:
            # Try parsing various date formats
            for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime(self.config["date_format"])
                except ValueError:
                    continue
            
            # If no format matches, return original string
            return date_str
        except Exception:
            return date_str
    
    def validate_priority(self, priority: str) -> bool:
        """Validate priority level."""
        return priority.lower() in self.config["priorities"]
    
    def validate_category(self, category: str) -> bool:
        """Validate category."""
        return category.lower() in self.config["categories"]


class TaskManager(PKMSManager):
    """Task management functionality."""
    
    def add_task(self, title: str, description: str = "", priority: str = "medium", 
                 due_date: str = "", category: str = "personal", tags: List[str] = None) -> None:
        """Add a new task with enhanced metadata."""
        if not self.validate_priority(priority):
            print(f"Warning: Invalid priority '{priority}'. Using 'medium'.")
            priority = "medium"
        
        if not self.validate_category(category):
            print(f"Warning: Invalid category '{category}'. Using 'personal'.")
            category = "personal"
        
        new_task = {
            'id': self.generate_id(self.tasks),
            'title': title,
            'description': description,
            'priority': priority.lower(),
            'category': category.lower(),
            'due_date': self.parse_date(due_date),
            'tags': tags or [],
            'status': 'pending',  # pending, in_progress, completed, cancelled
            'completed': False,
            'created_at': self.get_timestamp(),
            'updated_at': self.get_timestamp(),
            'dependencies': [],  # Task IDs this task depends on
            'notes': []  # Associated notes
        }
        
        self.tasks.append(new_task)
        self.save_data(self.tasks, TASKS_FILE)
        
        print(f"✓ Task added successfully (ID: {new_task['id']})")
        print(f"  Title: {title}")
        print(f"  Priority: {priority}")
        print(f"  Category: {category}")
        if due_date:
            print(f"  Due: {new_task['due_date']}")
    
    def list_tasks(self, status: str = "all", priority: str = "all", 
                   category: str = "all", show_completed: bool = True) -> None:
        """List tasks with filtering options."""
        filtered_tasks = self.tasks.copy()
        
        # Apply filters
        if status != "all":
            filtered_tasks = [t for t in filtered_tasks if t['status'] == status]
        
        if priority != "all":
            filtered_tasks = [t for t in filtered_tasks if t['priority'] == priority]
        
        if category != "all":
            filtered_tasks = [t for t in filtered_tasks if t['category'] == category]
        
        if not show_completed:
            filtered_tasks = [t for t in filtered_tasks if not t['completed']]
        
        # Sort by priority and due date
        priority_order = {p: i for i, p in enumerate(self.config["priorities"])}
        filtered_tasks.sort(key=lambda t: (
            priority_order.get(t['priority'], 999),
            t['due_date'] or '9999-12-31',
            t['created_at']
        ))
        
        if not filtered_tasks:
            print("No tasks found matching the criteria.")
            return
        
        print(f"\n{'='*80}")
        print(f"TASKS ({len(filtered_tasks)} found)")
        print(f"{'='*80}\n")
        
        for task in filtered_tasks:
            status_icon = self.get_status_icon(task)
            priority_indicator = self.get_priority_indicator(task['priority'])
            
            print(f"{status_icon} ID: {task['id']} {priority_indicator}")
            print(f"    Title: {task['title']}")
            print(f"    Category: {task['category'].title()}")
            print(f"    Status: {task['status'].replace('_', ' ').title()}")
            
            if task['description']:
                print(f"    Description: {task['description']}")
            
            if task['due_date']:
                due_status = self.get_due_status(task['due_date'])
                print(f"    Due: {task['due_date']} {due_status}")
            
            if task['tags']:
                print(f"    Tags: {', '.join(task['tags'])}")
            
            print(f"    Created: {task['created_at']}")
            print()
    
    def get_status_icon(self, task: Dict[str, Any]) -> str:
        """Get status icon for task."""
        icons = {
            'pending': '○',
            'in_progress': '◐',
            'completed': '✓',
            'cancelled': '✗'
        }
        return icons.get(task['status'], '○')
    
    def get_priority_indicator(self, priority: str) -> str:
        """Get priority indicator."""
        indicators = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🟠',
            'urgent': '🔴'
        }
        return indicators.get(priority, '🟡')
    
    def get_due_status(self, due_date: str) -> str:
        """Get due date status indicator."""
        if not due_date:
            return ""
        
        try:
            due = datetime.strptime(due_date, self.config["date_format"]).date()
            today = date.today()
            
            if due < today:
                return "⚠️ OVERDUE"
            elif due == today:
                return "📅 DUE TODAY"
            elif (due - today).days <= 3:
                return "⏰ DUE SOON"
            else:
                return ""
        except ValueError:
            return ""
    
    def update_task_status(self, task_id: int, status: str) -> None:
        """Update task status."""
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if status not in valid_statuses:
            print(f"Error: Invalid status. Use: {', '.join(valid_statuses)}")
            return
        
        for task in self.tasks:
            if task['id'] == task_id:
                old_status = task['status']
                task['status'] = status
                task['completed'] = (status == 'completed')
                task['updated_at'] = self.get_timestamp()
                
                self.save_data(self.tasks, TASKS_FILE)
                print(f"✓ Task {task_id} status updated: {old_status} → {status}")
                print(f"  Title: {task['title']}")
                return
        
        print(f"Error: Task {task_id} not found.")
    
    def complete_task(self, task_id: int) -> None:
        """Mark task as completed."""
        self.update_task_status(task_id, 'completed')
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_data(self.tasks, TASKS_FILE)
                print(f"✓ Task deleted: {deleted_task['title']}")
                return
        
        print(f"Error: Task {task_id} not found.")


class NoteManager(PKMSManager):
    """Note and knowledge management functionality."""
    
    def add_note(self, title: str, content: str = "", tags: List[str] = None, 
                 category: str = "personal", linked_tasks: List[int] = None) -> None:
        """Add a new note."""
        if not self.validate_category(category):
            print(f"Warning: Invalid category '{category}'. Using 'personal'.")
            category = "personal"
        
        new_note = {
            'id': self.generate_id(self.notes),
            'title': title,
            'content': content,
            'category': category.lower(),
            'tags': tags or [],
            'linked_tasks': linked_tasks or [],
            'created_at': self.get_timestamp(),
            'updated_at': self.get_timestamp()
        }
        
        self.notes.append(new_note)
        self.save_data(self.notes, NOTES_FILE)
        
        print(f"✓ Note added successfully (ID: {new_note['id']})")
        print(f"  Title: {title}")
        print(f"  Category: {category}")
        if tags:
            print(f"  Tags: {', '.join(tags)}")
    
    def list_notes(self, category: str = "all", tag: str = None) -> None:
        """List notes with filtering options."""
        filtered_notes = self.notes.copy()
        
        if category != "all":
            filtered_notes = [n for n in filtered_notes if n['category'] == category]
        
        if tag:
            filtered_notes = [n for n in filtered_notes if tag in n['tags']]
        
        # Sort by creation date (newest first)
        filtered_notes.sort(key=lambda n: n['created_at'], reverse=True)
        
        if not filtered_notes:
            print("No notes found matching the criteria.")
            return
        
        print(f"\n{'='*80}")
        print(f"NOTES ({len(filtered_notes)} found)")
        print(f"{'='*80}\n")
        
        for note in filtered_notes:
            print(f"📝 ID: {note['id']}")
            print(f"    Title: {note['title']}")
            print(f"    Category: {note['category'].title()}")
            
            if note['content']:
                # Show first 100 characters of content
                content_preview = note['content'][:100]
                if len(note['content']) > 100:
                    content_preview += "..."
                print(f"    Content: {content_preview}")
            
            if note['tags']:
                print(f"    Tags: {', '.join(note['tags'])}")
            
            if note['linked_tasks']:
                print(f"    Linked Tasks: {', '.join(map(str, note['linked_tasks']))}")
            
            print(f"    Created: {note['created_at']}")
            print()
    
    def view_note(self, note_id: int) -> None:
        """View full note content."""
        for note in self.notes:
            if note['id'] == note_id:
                print(f"\n{'='*80}")
                print(f"NOTE: {note['title']}")
                print(f"{'='*80}\n")
                print(f"ID: {note['id']}")
                print(f"Category: {note['category'].title()}")
                print(f"Created: {note['created_at']}")
                print(f"Updated: {note['updated_at']}")
                
                if note['tags']:
                    print(f"Tags: {', '.join(note['tags'])}")
                
                if note['linked_tasks']:
                    print(f"Linked Tasks: {', '.join(map(str, note['linked_tasks']))}")
                
                print(f"\nContent:\n{'-'*40}")
                print(note['content'])
                return
        
        print(f"Error: Note {note_id} not found.")
    
    def delete_note(self, note_id: int) -> None:
        """Delete a note."""
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                deleted_note = self.notes.pop(i)
                self.save_data(self.notes, NOTES_FILE)
                print(f"✓ Note deleted: {deleted_note['title']}")
                return
        
        print(f"Error: Note {note_id} not found.")


class SearchManager(PKMSManager):
    """Advanced search functionality."""
    
    def search_all(self, keyword: str, search_type: str = "all") -> None:
        """Search across tasks and notes."""
        keyword_lower = keyword.lower()
        results = {
            'tasks': [],
            'notes': []
        }
        
        # Search tasks
        if search_type in ["all", "tasks"]:
            for task in self.tasks:
                if self.matches_search(task, keyword_lower, 'task'):
                    results['tasks'].append(task)
        
        # Search notes
        if search_type in ["all", "notes"]:
            for note in self.notes:
                if self.matches_search(note, keyword_lower, 'note'):
                    results['notes'].append(note)
        
        # Display results
        total_results = len(results['tasks']) + len(results['notes'])
        
        if total_results == 0:
            print(f"No results found for '{keyword}'")
            return
        
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS for '{keyword}' ({total_results} found)")
        print(f"{'='*80}\n")
        
        # Show task results
        if results['tasks']:
            print(f"TASKS ({len(results['tasks'])} found):")
            print("-" * 40)
            for task in results['tasks']:
                status_icon = TaskManager.get_status_icon(self, task)
                print(f"{status_icon} [T{task['id']}] {task['title']}")
                if task['description'] and keyword_lower in task['description'].lower():
                    print(f"    Description: {task['description']}")
                if any(keyword_lower in tag.lower() for tag in task['tags']):
                    print(f"    Tags: {', '.join(task['tags'])}")
                print()
        
        # Show note results
        if results['notes']:
            print(f"NOTES ({len(results['notes'])} found):")
            print("-" * 40)
            for note in results['notes']:
                print(f"📝 [N{note['id']}] {note['title']}")
                if note['content'] and keyword_lower in note['content'].lower():
                    # Show context around the match
                    content_preview = self.get_content_context(note['content'], keyword_lower)
                    print(f"    Content: ...{content_preview}...")
                if any(keyword_lower in tag.lower() for tag in note['tags']):
                    print(f"    Tags: {', '.join(note['tags'])}")
                print()
    
    def matches_search(self, item: Dict[str, Any], keyword: str, item_type: str) -> bool:
        """Check if item matches search keyword."""
        search_fields = []
        
        if item_type == 'task':
            search_fields = [
                item.get('title', ''),
                item.get('description', ''),
                ' '.join(item.get('tags', [])),
                item.get('category', '')
            ]
        elif item_type == 'note':
            search_fields = [
                item.get('title', ''),
                item.get('content', ''),
                ' '.join(item.get('tags', [])),
                item.get('category', '')
            ]
        
        return any(keyword in field.lower() for field in search_fields)
    
    def get_content_context(self, content: str, keyword: str, context_chars: int = 50) -> str:
        """Get context around keyword match in content."""
        content_lower = content.lower()
        keyword_index = content_lower.find(keyword)
        
        if keyword_index == -1:
            return content[:100]
        
        start = max(0, keyword_index - context_chars)
        end = min(len(content), keyword_index + len(keyword) + context_chars)
        
        return content[start:end]


class ImportExportManager(PKMSManager):
    """Import and export functionality."""
    
    def export_data(self, format_type: str = "json", output_file: str = None) -> None:
        """Export all data to specified format."""
        if format_type not in ["json", "csv", "markdown"]:
            print("Error: Supported formats are: json, csv, markdown")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not output_file:
            output_file = f"pkms_export_{timestamp}.{format_type}"
        
        export_data = {
            'tasks': self.tasks,
            'notes': self.notes,
            'config': self.config,
            'exported_at': self.get_timestamp(),
            'version': '1.0'
        }
        
        if format_type == "json":
            self.export_json(export_data, output_file)
        elif format_type == "markdown":
            self.export_markdown(export_data, output_file)
        
        print(f"✓ Data exported to {output_file}")
    
    def export_json(self, data: Dict[str, Any], filename: str) -> None:
        """Export data as JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def export_markdown(self, data: Dict[str, Any], filename: str) -> None:
        """Export data as Markdown."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# PKMS Export - {data['exported_at']}\n\n")
            
            # Export tasks
            f.write("## Tasks\n\n")
            for task in data['tasks']:
                status = "✓" if task['completed'] else "○"
                f.write(f"### {status} {task['title']} (ID: {task['id']})\n\n")
                f.write(f"- **Priority:** {task['priority'].title()}\n")
                f.write(f"- **Category:** {task['category'].title()}\n")
                f.write(f"- **Status:** {task['status'].replace('_', ' ').title()}\n")
                
                if task['description']:
                    f.write(f"- **Description:** {task['description']}\n")
                
                if task['due_date']:
                    f.write(f"- **Due Date:** {task['due_date']}\n")
                
                if task['tags']:
                    f.write(f"- **Tags:** {', '.join(task['tags'])}\n")
                
                f.write(f"- **Created:** {task['created_at']}\n\n")
            
            # Export notes
            f.write("## Notes\n\n")
            for note in data['notes']:
                f.write(f"### 📝 {note['title']} (ID: {note['id']})\n\n")
                f.write(f"- **Category:** {note['category'].title()}\n")
                
                if note['tags']:
                    f.write(f"- **Tags:** {', '.join(note['tags'])}\n")
                
                f.write(f"- **Created:** {note['created_at']}\n\n")
                
                if note['content']:
                    f.write(f"{note['content']}\n\n")
                
                f.write("---\n\n")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI interface."""
    parser = argparse.ArgumentParser(
        description="Personal Knowledge Management System (PKMS)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pkms.py task add "Complete project" --priority high --due 2025-11-10
  python pkms.py task list --status pending --priority urgent
  python pkms.py note add "Meeting Notes" --content "Important decisions made"
  python pkms.py search "python" --type all
  python pkms.py export --format markdown
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Task commands
    task_parser = subparsers.add_parser('task', help='Task management')
    task_subparsers = task_parser.add_subparsers(dest='task_action')
    
    # Task add
    task_add = task_subparsers.add_parser('add', help='Add a new task')
    task_add.add_argument('title', help='Task title')
    task_add.add_argument('--description', '-d', default='', help='Task description')
    task_add.add_argument('--priority', '-p', default='medium', 
                         choices=['low', 'medium', 'high', 'urgent'], help='Task priority')
    task_add.add_argument('--due', help='Due date (YYYY-MM-DD)')
    task_add.add_argument('--category', '-c', default='personal',
                         choices=['personal', 'work', 'learning', 'project'], help='Task category')
    task_add.add_argument('--tags', nargs='*', help='Task tags')
    
    # Task list
    task_list = task_subparsers.add_parser('list', help='List tasks')
    task_list.add_argument('--status', default='all', 
                          choices=['all', 'pending', 'in_progress', 'completed', 'cancelled'])
    task_list.add_argument('--priority', default='all',
                          choices=['all', 'low', 'medium', 'high', 'urgent'])
    task_list.add_argument('--category', default='all',
                          choices=['all', 'personal', 'work', 'learning', 'project'])
    task_list.add_argument('--hide-completed', action='store_true',
                          help='Hide completed tasks')
    
    # Task update
    task_update = task_subparsers.add_parser('update', help='Update task status')
    task_update.add_argument('id', type=int, help='Task ID')
    task_update.add_argument('status', choices=['pending', 'in_progress', 'completed', 'cancelled'])
    
    # Task complete
    task_complete = task_subparsers.add_parser('complete', help='Mark task as completed')
    task_complete.add_argument('id', type=int, help='Task ID')
    
    # Task delete
    task_delete = task_subparsers.add_parser('delete', help='Delete a task')
    task_delete.add_argument('id', type=int, help='Task ID')
    
    # Note commands
    note_parser = subparsers.add_parser('note', help='Note management')
    note_subparsers = note_parser.add_subparsers(dest='note_action')
    
    # Note add
    note_add = note_subparsers.add_parser('add', help='Add a new note')
    note_add.add_argument('title', help='Note title')
    note_add.add_argument('--content', '-c', default='', help='Note content')
    note_add.add_argument('--category', default='personal',
                         choices=['personal', 'work', 'learning', 'project'], help='Note category')
    note_add.add_argument('--tags', nargs='*', help='Note tags')
    note_add.add_argument('--link-tasks', nargs='*', type=int, help='Link to task IDs')
    
    # Note list
    note_list = note_subparsers.add_parser('list', help='List notes')
    note_list.add_argument('--category', default='all',
                          choices=['all', 'personal', 'work', 'learning', 'project'])
    note_list.add_argument('--tag', help='Filter by tag')
    
    # Note view
    note_view = note_subparsers.add_parser('view', help='View full note')
    note_view.add_argument('id', type=int, help='Note ID')
    
    # Note delete
    note_delete = note_subparsers.add_parser('delete', help='Delete a note')
    note_delete.add_argument('id', type=int, help='Note ID')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks and notes')
    search_parser.add_argument('keyword', help='Search keyword')
    search_parser.add_argument('--type', default='all', choices=['all', 'tasks', 'notes'],
                              help='Search type')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--format', default='json', choices=['json', 'markdown'],
                              help='Export format')
    export_parser.add_argument('--output', help='Output filename')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    return parser


def show_stats(pkms: PKMSManager) -> None:
    """Show system statistics."""
    task_stats = {
        'total': len(pkms.tasks),
        'pending': len([t for t in pkms.tasks if t['status'] == 'pending']),
        'in_progress': len([t for t in pkms.tasks if t['status'] == 'in_progress']),
        'completed': len([t for t in pkms.tasks if t['status'] == 'completed']),
        'overdue': 0
    }
    
    # Count overdue tasks
    today = date.today()
    for task in pkms.tasks:
        if task['due_date'] and task['status'] not in ['completed', 'cancelled']:
            try:
                due = datetime.strptime(task['due_date'], pkms.config["date_format"]).date()
                if due < today:
                    task_stats['overdue'] += 1
            except ValueError:
                pass
    
    note_stats = {
        'total': len(pkms.notes),
        'categories': len(set(note['category'] for note in pkms.notes)),
        'tags': len(set(tag for note in pkms.notes for tag in note['tags']))
    }
    
    print(f"\n{'='*60}")
    print("PKMS STATISTICS")
    print(f"{'='*60}\n")
    
    print("📋 TASKS:")
    print(f"  Total: {task_stats['total']}")
    print(f"  Pending: {task_stats['pending']}")
    print(f"  In Progress: {task_stats['in_progress']}")
    print(f"  Completed: {task_stats['completed']}")
    print(f"  Overdue: {task_stats['overdue']}")
    
    print("\n📝 NOTES:")
    print(f"  Total: {note_stats['total']}")
    print(f"  Categories: {note_stats['categories']}")
    print(f"  Unique Tags: {note_stats['tags']}")
    
    if task_stats['total'] > 0:
        completion_rate = (task_stats['completed'] / task_stats['total']) * 100
        print(f"\n📊 Completion Rate: {completion_rate:.1f}%")


def main():
    """Main entry point for the PKMS application."""
    parser = create_parser()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Initialize managers
    task_manager = TaskManager()
    note_manager = NoteManager()
    search_manager = SearchManager()
    export_manager = ImportExportManager()
    
    try:
        # Handle task commands
        if args.command == 'task':
            if args.task_action == 'add':
                task_manager.add_task(
                    title=args.title,
                    description=args.description,
                    priority=args.priority,
                    due_date=args.due or '',
                    category=args.category,
                    tags=args.tags or []
                )
            elif args.task_action == 'list':
                task_manager.list_tasks(
                    status=args.status,
                    priority=args.priority,
                    category=args.category,
                    show_completed=not args.hide_completed
                )
            elif args.task_action == 'update':
                task_manager.update_task_status(args.id, args.status)
            elif args.task_action == 'complete':
                task_manager.complete_task(args.id)
            elif args.task_action == 'delete':
                task_manager.delete_task(args.id)
        
        # Handle note commands
        elif args.command == 'note':
            if args.note_action == 'add':
                note_manager.add_note(
                    title=args.title,
                    content=args.content,
                    tags=args.tags or [],
                    category=args.category,
                    linked_tasks=args.link_tasks or []
                )
            elif args.note_action == 'list':
                note_manager.list_notes(
                    category=args.category,
                    tag=args.tag
                )
            elif args.note_action == 'view':
                note_manager.view_note(args.id)
            elif args.note_action == 'delete':
                note_manager.delete_note(args.id)
        
        # Handle search command
        elif args.command == 'search':
            search_manager.search_all(args.keyword, args.type)
        
        # Handle export command
        elif args.command == 'export':
            export_manager.export_data(args.format, args.output)
        
        # Handle stats command
        elif args.command == 'stats':
            show_stats(task_manager)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()