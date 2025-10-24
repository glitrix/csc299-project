# Task Manager

A simple command-line application for managing tasks with Markdown-based Personal Knowledge Management (PKM) storage.

## Features

- Add tasks with title and optional description
- List all tasks
- Search tasks by keyword
- Mark tasks as complete
- Persistent storage in Markdown format (Obsidian-compatible)
- Each task stored as an individual Markdown file with YAML frontmatter

## Requirements

- Python 3.6 or higher (no external dependencies required)

## Installation

No installation required! This application uses only Python standard library modules.

## Usage

### Running the Application

Navigate to the `tasks1` directory and use the following commands:

**Note:** Use `py` instead of `python` on Windows if you encounter Python not found errors.

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

Tasks are stored as individual Markdown files in the `vault/` directory. Each task is saved with YAML frontmatter, making them compatible with Obsidian and other PKM tools.

### Markdown File Structure

Each task is stored with the following fields in YAML frontmatter:
- `id`: Unique identifier (auto-generated)
- `title`: Task title (required)
- `description`: Task description (optional)
- `completed`: Boolean status (true/false)
- `created_at`: Timestamp when task was created

Example task file (`vault/1-buy-groceries.md`):
```markdown
---
id: 1
title: "Buy groceries"
description: "Milk, eggs, bread"
completed: false
created_at: "2025-10-15 14:30:00"
---

# Buy groceries

Milk, eggs, bread
```

### File Naming Convention

Tasks are automatically saved with the pattern: `{id}-{slug}.md`
- Example: `1-buy-groceries.md`, `2-study-python.md`

### Obsidian Integration

You can open the `vault/` folder in Obsidian to:
- View and edit tasks in a rich Markdown editor
- Link tasks together using `[[Task Name]]` syntax
- Add tags, images, and other Markdown features
- Use Obsidian's search and graph view

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
- **Python not found**: Use `py` instead of `python` on Windows systems.

## License

This is a prototype application created for educational purposes.
