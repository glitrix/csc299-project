# Task Manager

A simple command-line application for managing tasks with JSON storage.

## Features

- Add tasks with title and optional description
- List all tasks
- Search tasks by keyword
- Mark tasks as complete
- Persistent storage in JSON format

## Requirements

- Python 3.6 or higher (no external dependencies required)

## Installation

No installation required! This application uses only Python standard library modules.

## Usage

### Running the Application

Navigate to the `tasks1` directory and use the following commands:

### Add a Task

```bash
python tasks.py add "Task title" "Optional description"
```

Example:
```bash
python tasks.py add "Buy groceries" "Milk, eggs, bread"
python tasks.py add "Study Python"
```

### List All Tasks

```bash
python tasks.py list
```

This displays all tasks with their ID, title, description, completion status, and creation date.

### Search Tasks

```bash
python tasks.py search "keyword"
```

Example:
```bash
python tasks.py search "groceries"
```

Searches for the keyword in both task titles and descriptions.

### Mark Task as Complete

```bash
python tasks.py complete <task_id>
```

Example:
```bash
python tasks.py complete 1
```

### Show Help

```bash
python tasks.py help
```

## Data Storage

Tasks are stored in a file called `tasks.json` in the same directory as `tasks.py`. This file is automatically created when you add your first task.

### JSON Structure

Each task is stored with the following fields:
- `id`: Unique identifier (auto-generated)
- `title`: Task title (required)
- `description`: Task description (optional)
- `completed`: Boolean status (true/false)
- `created_at`: Timestamp when task was created

Example `tasks.json`:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-10-15 14:30:00"
  },
  {
    "id": 2,
    "title": "Study Python",
    "description": "",
    "completed": true,
    "created_at": "2025-10-15 15:00:00"
  }
]
```

## Examples

Complete workflow example:

```bash
# Add some tasks
python tasks.py add "Complete assignment" "CSC299 project"
python tasks.py add "Read chapter 5" "Data structures book"
python tasks.py add "Email professor"

# List all tasks
python tasks.py list

# Search for specific tasks
python tasks.py search "chapter"

# Mark a task as complete
python tasks.py complete 1

# List tasks again to see the updated status
python tasks.py list
```

## Troubleshooting

- **"No tasks found"**: You haven't added any tasks yet. Use `python tasks.py add` to create your first task.
- **"Task ID not found"**: Make sure you're using the correct task ID shown in the list command.
- **"Error reading tasks file"**: The `tasks.json` file may be corrupted. You can delete it to start fresh.

## License

This is a prototype application created for educational purposes.
