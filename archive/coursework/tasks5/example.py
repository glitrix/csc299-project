"""
Example usage of the Task Manager.

This script demonstrates how to use the TaskManager class programmatically.
"""
from task_manager import TaskManager


def main():
    """Demonstrate task manager functionality."""
    
    # Initialize the task manager (uses 'tasks.json' by default)
    print("=" * 60)
    print("Task Manager Demo".center(60))
    print("=" * 60 + "\n")
    
    manager = TaskManager("demo_tasks.json")
    
    # Create some tasks
    print("1. Creating tasks...")
    task1 = manager.create_task(
        title="Complete project documentation",
        description="Write comprehensive README and API docs",
        status="in-progress"
    )
    print(f"   Created: {task1.title} (ID: {task1.id})")
    
    task2 = manager.create_task(
        title="Review pull requests",
        description="Review and merge pending PRs",
        status="pending"
    )
    print(f"   Created: {task2.title} (ID: {task2.id})")
    
    task3 = manager.create_task(
        title="Fix bug #123",
        description="Critical bug in login system",
        status="completed"
    )
    print(f"   Created: {task3.title} (ID: {task3.id})")
    
    # List all tasks
    print("\n2. Listing all tasks...")
    all_tasks = manager.get_all_tasks()
    for task in all_tasks:
        print(f"   [{task.status:12}] {task.title}")
    
    # Get tasks by status
    print("\n3. Getting pending tasks...")
    pending = manager.get_tasks_by_status("pending")
    print(f"   Found {len(pending)} pending task(s):")
    for task in pending:
        print(f"   - {task.title}")
    
    # Update a task
    print(f"\n4. Updating task '{task1.title}'...")
    manager.update_task(
        task1.id,
        status="completed",
        description="Documentation is now complete with examples"
    )
    updated_task = manager.get_task(task1.id)
    print(f"   New status: {updated_task.status}")
    print(f"   Updated description: {updated_task.description}")
    
    # Search for tasks
    print("\n5. Searching for tasks containing 'bug'...")
    results = manager.search_tasks("bug")
    print(f"   Found {len(results)} result(s):")
    for task in results:
        print(f"   - {task.title}")
    
    # Get statistics
    print("\n6. Task Statistics:")
    stats = manager.get_statistics()
    print(f"   Total tasks:    {stats['total']}")
    print(f"   Pending:        {stats['pending']}")
    print(f"   In Progress:    {stats['in_progress']}")
    print(f"   Completed:      {stats['completed']}")
    
    # Delete a task
    print(f"\n7. Deleting task '{task2.title}'...")
    if manager.delete_task(task2.id):
        print("   Task deleted successfully!")
    
    # Clear completed tasks
    print("\n8. Clearing completed tasks...")
    cleared = manager.clear_completed_tasks()
    print(f"   Removed {cleared} completed task(s)")
    
    # Final task list
    print("\n9. Final task list:")
    remaining = manager.get_all_tasks()
    if remaining:
        for task in remaining:
            print(f"   [{task.status:12}] {task.title}")
    else:
        print("   No tasks remaining!")
    
    print("\n" + "=" * 60)
    print("Demo Complete!".center(60))
    print("=" * 60)
    print("\nTask data has been saved to 'demo_tasks.json'")
    print("Run 'python cli.py' to start the interactive CLI\n")


if __name__ == "__main__":
    main()
