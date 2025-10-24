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

import sys
from typing import List, Dict, Any, Optional
import storage_markdown


def add_task(title: str, description: str = "") -> None:
    """Add a new task."""
    task_id, file_path = storage_markdown.save_task(title, description)
    
    print(f"✓ Task added successfully (ID: {task_id})")
    print(f"  Title: {title}")


def list_tasks() -> None:
    """List all tasks."""
    tasks = storage_markdown.list_tasks()
    
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
    matching_tasks = storage_markdown.search_tasks(keyword)
    
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
    # First check if task exists and if it's already completed
    tasks = storage_markdown.list_tasks()
    task_found = None
    
    for task in tasks:
        if task['id'] == task_id:
            task_found = task
            break
    
    if not task_found:
        print(f"Error: Task {task_id} not found.")
        return
    
    if task_found['completed']:
        print(f"Task {task_id} is already completed.")
        return
    
    # Mark task as complete
    if storage_markdown.mark_complete(task_id):
        print(f"✓ Task {task_id} marked as complete: {task_found['title']}")
    else:
        print(f"Error: Could not mark task {task_id} as complete.")


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
