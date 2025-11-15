# Task Manager with JSON Storage

A simple yet powerful task manager that stores all data in JSON files. Perfect for personal task management, project tracking, or as a learning example for file-based data persistence.

## Features

- ✅ **Create, Read, Update, Delete (CRUD)** operations for tasks
- 💾 **JSON file storage** - all data persists in human-readable JSON format
- 🔍 **Search functionality** - find tasks by title or description
- 📊 **Statistics** - track task completion and status
- 🎯 **Task statuses** - pending, in-progress, completed
- ⏰ **Timestamps** - automatic tracking of creation and update times
- 🎨 **Interactive CLI** - user-friendly command-line interface
- 📝 **Programmatic API** - use as a library in your own code

## Project Structure

```
Task5/
├── task.py           # Task class definition
├── storage.py        # JSON storage handler
├── task_manager.py   # Main task manager logic
├── cli.py            # Command-line interface
├── example.py        # Usage examples
├── README.md         # This file
└── tasks.json        # Generated task data file
```

## Installation

No external dependencies required! This project uses only Python standard library modules.

Requirements:
- Python 3.7 or higher

Simply clone or download the files to your local machine.

## Usage

### Interactive CLI Mode

Start the interactive command-line interface:

```bash
python cli.py
```

Available commands:
- `add <title>` - Add a new task
- `list [status]` - List all tasks or filter by status
- `view <task_id>` - View detailed task information
- `update <task_id>` - Update a task
- `delete <task_id>` - Delete a task
- `complete <task_id>` - Mark a task as completed
- `search <query>` - Search tasks by title/description
- `stats` - Show task statistics
- `clear` - Clear all completed tasks
- `help` - Show help message
- `exit` - Exit the application

### Programmatic Usage

Use the TaskManager class in your own Python code:

```python
from task_manager import TaskManager

# Initialize the manager
manager = TaskManager("my_tasks.json")

# Create a task
task = manager.create_task(
    title="Complete homework",
    description="Math assignment chapter 5",
    status="pending"
)

# List all tasks
tasks = manager.get_all_tasks()
for task in tasks:
    print(f"{task.title} - {task.status}")

# Update a task
manager.update_task(task.id, status="completed")

# Search tasks
results = manager.search_tasks("homework")

# Get statistics
stats = manager.get_statistics()
print(f"Total: {stats['total']}, Completed: {stats['completed']}")
```

### Run the Demo

See examples of all functionality:

```bash
python example.py
```

## Task Properties

Each task has the following properties:

- **id** - Unique identifier (automatically generated)
- **title** - Task title (required)
- **description** - Detailed description (optional)
- **status** - Current status: `pending`, `in-progress`, or `completed`
- **created_at** - ISO 8601 timestamp of creation
- **updated_at** - ISO 8601 timestamp of last update

## JSON Data Format

Tasks are stored in a simple JSON array format:

```json
[
  {
    "id": "20251115143052123456",
    "title": "Complete project",
    "description": "Finish the task manager implementation",
    "status": "in-progress",
    "created_at": "2025-11-15T14:30:52.123456",
    "updated_at": "2025-11-15T15:45:10.789012"
  }
]
```

## API Reference

### TaskManager Class

**Constructor:**
- `TaskManager(storage_file="tasks.json")` - Initialize with optional custom file path

**Methods:**
- `create_task(title, description="", status="pending")` - Create a new task
- `get_task(task_id)` - Retrieve a specific task
- `get_all_tasks()` - Get all tasks
- `get_tasks_by_status(status)` - Filter tasks by status
- `update_task(task_id, title=None, description=None, status=None)` - Update task properties
- `delete_task(task_id)` - Delete a task
- `search_tasks(query)` - Search in titles and descriptions
- `clear_completed_tasks()` - Remove all completed tasks
- `get_statistics()` - Get task counts by status

### Task Class

**Constructor:**
- `Task(title, description="", status="pending", task_id=None, created_at=None, updated_at=None)`

**Methods:**
- `to_dict()` - Convert to dictionary for JSON serialization
- `from_dict(data)` - Create Task from dictionary (class method)
- `update_timestamp()` - Update the last modified time

### JSONStorage Class

**Constructor:**
- `JSONStorage(filepath="tasks.json")` - Initialize with file path

**Methods:**
- `load_tasks()` - Load tasks from file
- `save_tasks(tasks)` - Save tasks to file
- `backup(backup_path=None)` - Create a backup of the tasks file

## Examples

### Example 1: Quick Task Management

```python
manager = TaskManager()

# Add tasks
manager.create_task("Buy groceries", "Milk, eggs, bread")
manager.create_task("Call dentist", status="pending")

# Mark as complete
tasks = manager.get_tasks_by_status("pending")
if tasks:
    manager.update_task(tasks[0].id, status="completed")
```

### Example 2: Task Tracking

```python
manager = TaskManager("project_tasks.json")

# Create project tasks
for i in range(1, 6):
    manager.create_task(
        f"Feature {i}",
        f"Implement feature number {i}",
        "pending"
    )

# Track progress
stats = manager.get_statistics()
completion = (stats['completed'] / stats['total']) * 100
print(f"Project is {completion:.1f}% complete")
```

## Error Handling

The task manager includes built-in error handling for:
- Missing or corrupted JSON files
- Invalid task IDs
- File I/O errors
- JSON parsing errors

Errors are logged to the console with descriptive messages.

## Data Persistence

All task data is automatically saved to the JSON file after every operation:
- Creating a task
- Updating a task
- Deleting a task
- Clearing completed tasks

This ensures your data is never lost, even if the application crashes.

## Customization

You can easily customize the task manager:

1. **Add new task properties** - Modify the `Task` class
2. **Change status values** - Update validation in `TaskManager`
3. **Add new operations** - Extend the `TaskManager` class
4. **Custom storage backends** - Implement new storage classes

## License

Free to use for educational and personal projects.

## Contributing

This is an educational project. Feel free to fork and modify for your needs!

## Author

Created as a demonstration of file-based data persistence in Python.

---

**Happy Task Managing! 📋✨**
