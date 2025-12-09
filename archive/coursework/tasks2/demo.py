#!/usr/bin/env python3
"""
PKMS Demo Script

This script demonstrates the key features of the Personal Knowledge Management System.
Run this script to see how the PKMS works with sample data.
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and display its output with description."""
    print(f"\n{'='*60}")
    print(f"DEMO: {description}")
    print(f"Command: py pkms.py {command}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            f"py pkms.py {command}",
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Error running command: {e}")
    
    input("Press Enter to continue...")

def main():
    """Run the PKMS demonstration."""
    print("Personal Knowledge Management System (PKMS) Demo")
    print("This demo will show you the key features of the PKMS")
    print("\nPress Ctrl+C at any time to exit the demo")
    
    try:
        # Clear any existing demo data by showing initial stats
        run_command("stats", "Check initial system state")
        
        # Task management demo
        run_command(
            'task add "Learn Python advanced concepts" --priority high --due 2025-11-15 --category learning --tags python advanced',
            "Add a high-priority learning task"
        )
        
        run_command(
            'task add "Write project documentation" --priority medium --due 2025-11-20 --category work --tags documentation writing',
            "Add a work task with medium priority"
        )
        
        run_command(
            'task add "Buy groceries" --priority low --category personal --tags shopping errands',
            "Add a personal task without due date"
        )
        
        run_command("task list", "List all tasks")
        
        # Note management demo
        run_command(
            'note add "Python Learning Notes" --content "Key concepts: decorators, generators, context managers, metaclasses" --tags python learning --category learning',
            "Add a learning note"
        )
        
        run_command(
            'note add "Project Ideas" --content "1. Task management app\n2. Personal finance tracker\n3. Learning progress dashboard" --tags ideas projects --category work',
            "Add project ideas note"
        )
        
        run_command("note list", "List all notes")
        
        # Search demo
        run_command('search "python"', "Search for 'python' across all items")
        
        run_command('search "project" --type notes', "Search for 'project' in notes only")
        
        # Task status updates
        run_command("task update 1 in_progress", "Mark learning task as in progress")
        
        run_command("task complete 3", "Complete the groceries task")
        
        # View detailed note
        run_command("note view 1", "View full content of the learning note")
        
        # Advanced filtering
        run_command("task list --status pending --priority high", "List pending high-priority tasks")
        
        run_command("note list --category learning", "List learning-related notes")
        
        # Statistics
        run_command("stats", "View updated system statistics")
        
        # Export demo
        run_command("export --format markdown --output demo_export.md", "Export data to Markdown format")
        
        print("\n" + "="*60)
        print("DEMO COMPLETE!")
        print("="*60)
        print("You've seen the key features of the PKMS:")
        print("✓ Task management with priorities and due dates")
        print("✓ Note-taking with content and linking")
        print("✓ Tagging and categorization")
        print("✓ Advanced search across all content")
        print("✓ Status tracking and updates")
        print("✓ Filtering and sorting options")
        print("✓ Statistics and analytics")
        print("✓ Data export capabilities")
        print("\nTry exploring the system yourself with 'py pkms.py --help'")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Thanks for trying the PKMS!")
    except Exception as e:
        print(f"\nDemo error: {e}")

if __name__ == "__main__":
    main()