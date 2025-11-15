"""
Command-line interface for the Task Manager.
"""
import sys
from task_manager import TaskManager


class TaskManagerCLI:
    """Command-line interface for task management."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.manager = TaskManager()
        self.commands = {
            "add": self.add_task,
            "list": self.list_tasks,
            "view": self.view_task,
            "update": self.update_task,
            "delete": self.delete_task,
            "complete": self.complete_task,
            "search": self.search_tasks,
            "stats": self.show_statistics,
            "clear": self.clear_completed,
            "help": self.show_help,
            "exit": self.exit_app
        }
    
    def run(self):
        """Start the CLI application."""
        print("=" * 60)
        print("Task Manager - JSON Storage Edition".center(60))
        print("=" * 60)
        print("\nType 'help' to see available commands.\n")
        
        while True:
            try:
                command = input("task-manager> ").strip().lower()
                if not command:
                    continue
                
                parts = command.split(maxsplit=1)
                cmd = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def add_task(self, args: str):
        """Add a new task."""
        if not args:
            print("Usage: add <title>")
            return
        
        print("\nCreating new task...")
        title = args
        description = input("Description (optional): ").strip()
        status = input("Status (pending/in-progress/completed) [pending]: ").strip() or "pending"
        
        task = self.manager.create_task(title, description, status)
        print(f"\n✓ Task created successfully!")
        print(f"  ID: {task.id}")
        print(f"  Title: {task.title}")
        print(f"  Status: {task.status}\n")
    
    def list_tasks(self, args: str):
        """List all tasks or filter by status."""
        if args:
            tasks = self.manager.get_tasks_by_status(args)
            print(f"\nTasks with status '{args}':")
        else:
            tasks = self.manager.get_all_tasks()
            print("\nAll Tasks:")
        
        if not tasks:
            print("  No tasks found.\n")
            return
        
        print("-" * 60)
        for task in tasks:
            print(f"  [{task.status.upper():12}] {task.title}")
            print(f"  ID: {task.id}")
            if task.description:
                print(f"  Description: {task.description[:50]}...")
            print("-" * 60)
        print()
    
    def view_task(self, args: str):
        """View detailed information about a task."""
        if not args:
            print("Usage: view <task_id>")
            return
        
        task = self.manager.get_task(args)
        if not task:
            print(f"Task with ID '{args}' not found.\n")
            return
        
        print("\n" + "=" * 60)
        print(f"Task Details")
        print("=" * 60)
        print(f"ID:          {task.id}")
        print(f"Title:       {task.title}")
        print(f"Description: {task.description or '(none)'}")
        print(f"Status:      {task.status}")
        print(f"Created:     {task.created_at}")
        print(f"Updated:     {task.updated_at}")
        print("=" * 60 + "\n")
    
    def update_task(self, args: str):
        """Update a task."""
        if not args:
            print("Usage: update <task_id>")
            return
        
        task = self.manager.get_task(args)
        if not task:
            print(f"Task with ID '{args}' not found.\n")
            return
        
        print(f"\nUpdating task: {task.title}")
        print("Leave blank to keep current value.\n")
        
        title = input(f"Title [{task.title}]: ").strip()
        description = input(f"Description [{task.description}]: ").strip()
        status = input(f"Status [{task.status}]: ").strip()
        
        success = self.manager.update_task(
            args,
            title=title if title else None,
            description=description if description else None,
            status=status if status else None
        )
        
        if success:
            print("\n✓ Task updated successfully!\n")
        else:
            print("\n✗ Failed to update task.\n")
    
    def delete_task(self, args: str):
        """Delete a task."""
        if not args:
            print("Usage: delete <task_id>")
            return
        
        task = self.manager.get_task(args)
        if not task:
            print(f"Task with ID '{args}' not found.\n")
            return
        
        confirm = input(f"Delete task '{task.title}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            if self.manager.delete_task(args):
                print("\n✓ Task deleted successfully!\n")
            else:
                print("\n✗ Failed to delete task.\n")
        else:
            print("\nDeletion cancelled.\n")
    
    def complete_task(self, args: str):
        """Mark a task as completed."""
        if not args:
            print("Usage: complete <task_id>")
            return
        
        if self.manager.update_task(args, status="completed"):
            print("\n✓ Task marked as completed!\n")
        else:
            print(f"\n✗ Task with ID '{args}' not found.\n")
    
    def search_tasks(self, args: str):
        """Search for tasks."""
        if not args:
            print("Usage: search <query>")
            return
        
        tasks = self.manager.search_tasks(args)
        print(f"\nSearch results for '{args}':")
        
        if not tasks:
            print("  No matching tasks found.\n")
            return
        
        print("-" * 60)
        for task in tasks:
            print(f"  [{task.status.upper():12}] {task.title}")
            print(f"  ID: {task.id}")
            print("-" * 60)
        print()
    
    def show_statistics(self, args: str):
        """Show task statistics."""
        stats = self.manager.get_statistics()
        
        print("\n" + "=" * 60)
        print("Task Statistics".center(60))
        print("=" * 60)
        print(f"Total Tasks:       {stats['total']}")
        print(f"Pending:           {stats['pending']}")
        print(f"In Progress:       {stats['in_progress']}")
        print(f"Completed:         {stats['completed']}")
        print("=" * 60 + "\n")
    
    def clear_completed(self, args: str):
        """Clear all completed tasks."""
        confirm = input("Delete all completed tasks? (yes/no): ").strip().lower()
        if confirm == "yes":
            count = self.manager.clear_completed_tasks()
            print(f"\n✓ Removed {count} completed task(s).\n")
        else:
            print("\nOperation cancelled.\n")
    
    def show_help(self, args: str):
        """Show help information."""
        print("\n" + "=" * 60)
        print("Available Commands".center(60))
        print("=" * 60)
        print("  add <title>           - Add a new task")
        print("  list [status]         - List all tasks or filter by status")
        print("  view <task_id>        - View detailed task information")
        print("  update <task_id>      - Update a task")
        print("  delete <task_id>      - Delete a task")
        print("  complete <task_id>    - Mark a task as completed")
        print("  search <query>        - Search tasks by title/description")
        print("  stats                 - Show task statistics")
        print("  clear                 - Clear all completed tasks")
        print("  help                  - Show this help message")
        print("  exit                  - Exit the application")
        print("=" * 60 + "\n")
    
    def exit_app(self, args: str):
        """Exit the application."""
        print("\nGoodbye!")
        sys.exit(0)


def main():
    """Main entry point for the CLI application."""
    cli = TaskManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
