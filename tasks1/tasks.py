#!/usr/bin/env python3
"""
Task Manager - Command-line application for managing tasks

Features:
- Add tasks with title and description
- List all tasks
- Search tasks by keyword
- Mark tasks as complete
- JSON file storage

Usage:
    python tasks.py add "Task title" "Task description"
    python tasks.py list
    python tasks.py search "keyword"
    python tasks.py complete <task_id>
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configuration
TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from JSON file."""
    if not TASKS_FILE.exists():
        return []
    
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: Could not read tasks file. Starting with empty task list.")
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Save tasks to JSON file."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def generate_id(tasks: List[Dict[str, Any]]) -> int:
    """Generate a new task ID."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_task(title: str, description: str = "") -> None:
    """Add a new task."""
    tasks = load_tasks()
    
    new_task = {
        'id': generate_id(tasks),
        'title': title,
        'description': description,
        'completed': False,
        'created_at': get_timestamp()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    
    print(f"✓ Task added successfully (ID: {new_task['id']})")
    print(f"  Title: {title}")


def list_tasks() -> None:
    """List all tasks."""
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found.")
        return
    
    print(f"\n{'='*60}")
    print(f"TASKS ({len(tasks)} total)")
    print(f"{'='*60}\n")
    
    for task in tasks:
        status = "✓" if task['completed'] else "○"
        print(f"[{status}] ID: {task['id']}")
        print(f"    Title: {task['title']}")
        if task['description']:
            print(f"    Description: {task['description']}")
        print(f"    Created: {task['created_at']}")
        print()


def search_tasks(keyword: str) -> None:
    """Search tasks by keyword in title or description."""
    tasks = load_tasks()
    keyword_lower = keyword.lower()
    
    matching_tasks = [
        task for task in tasks
        if keyword_lower in task['title'].lower() or 
           keyword_lower in task['description'].lower()
    ]
    
    if not matching_tasks:
        print(f"No tasks found matching '{keyword}'")
        return
    
    print(f"\n{'='*60}")
    print(f"SEARCH RESULTS for '{keyword}' ({len(matching_tasks)} found)")
    print(f"{'='*60}\n")
    
    for task in matching_tasks:
        status = "✓" if task['completed'] else "○"
        print(f"[{status}] ID: {task['id']}")
        print(f"    Title: {task['title']}")
        if task['description']:
            print(f"    Description: {task['description']}")
        print(f"    Created: {task['created_at']}")
        print()


def complete_task(task_id: int) -> None:
    """Mark a task as complete."""
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            if task['completed']:
                print(f"Task {task_id} is already completed.")
            else:
                task['completed'] = True
                save_tasks(tasks)
                print(f"✓ Task {task_id} marked as complete: {task['title']}")
            return
    
    print(f"Error: Task {task_id} not found.")


def show_help() -> None:
    """Display help information."""
    help_text = """
Task Manager - Command-line task management application

USAGE:
    python tasks.py <command> [arguments]

COMMANDS:
    add <title> [description]    Add a new task
    list                         List all tasks
    search <keyword>             Search tasks by keyword
    complete <task_id>           Mark a task as complete
    help                         Show this help message

EXAMPLES:
    python tasks.py add "Buy groceries" "Milk, eggs, bread"
    python tasks.py list
    python tasks.py search "groceries"
    python tasks.py complete 1
"""
    print(help_text)


def main():
    """Main entry point for the application."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Task title required.")
            print("Usage: python tasks.py add <title> [description]")
            sys.exit(1)
        
        title = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        add_task(title, description)
    
    elif command == "list":
        list_tasks()
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Search keyword required.")
            print("Usage: python tasks.py search <keyword>")
            sys.exit(1)
        
        keyword = sys.argv[2]
        search_tasks(keyword)
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Task ID required.")
            print("Usage: python tasks.py complete <task_id>")
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
            complete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            sys.exit(1)
    
    elif command == "help":
        show_help()
    
    else:
        print(f"Error: Unknown command '{command}'")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
