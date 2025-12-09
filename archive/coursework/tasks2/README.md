# Personal Knowledge Management System (PKMS) - Tasks2

An enhanced command-line application for managing tasks, notes, and knowledge items with advanced features for personal knowledge management.

## Features

### Task Management
- Create tasks with priorities (low, medium, high, urgent)
- Set due dates and categories 
- Track task status (pending, in_progress, completed, cancelled)
- Tag system for organization
- Task dependencies and relationships
- Visual priority indicators and status icons

### Note Management
- Create and manage notes with rich content
- Link notes to tasks
- Categorize notes by type
- Tag system for easy organization
- Full-text search capabilities

### Advanced Features
- Cross-platform search across tasks and notes
- Multiple export formats (JSON, Markdown)
- Statistics and analytics
- Flexible filtering and sorting
- Data integrity and backup

## Requirements

- Python 3.7 or higher (no external dependencies required)
- Uses only Python standard library modules

## Installation

No installation required! This application uses only Python standard library modules.

## Quick Start

### Initialize the System

The PKMS will automatically create necessary data files on first use:

```bash
python pkms.py stats
```

### Add Your First Task

```bash
python pkms.py task add "Complete PKMS project" --priority high --due 2025-11-10 --category work --tags python development
```

### Add a Note

```bash
python pkms.py note add "Python Learning Notes" --content "Key concepts and best practices" --tags python learning --category learning
```

### List Tasks

```bash
python pkms.py task list
```

## Detailed Usage

### Task Management

#### Add a Task

```bash
python pkms.py task add "Task title" [options]
```

**Options:**
- `--description, -d`: Task description
- `--priority, -p`: Priority level (low, medium, high, urgent)
- `--due`: Due date in YYYY-MM-DD format
- `--category, -c`: Category (personal, work, learning, project)
- `--tags`: Space-separated list of tags

**Examples:**
```bash
python pkms.py task add "Buy groceries" --description "Milk, eggs, bread" --priority medium --due 2025-11-05 --category personal --tags shopping errands

python pkms.py task add "Code review" --priority high --category work --tags review code

python pkms.py task add "Study algorithms" --due 2025-11-15 --category learning --tags study algorithms computer-science
```

#### List Tasks

```bash
python pkms.py task list [options]
```

**Options:**
- `--status`: Filter by status (all, pending, in_progress, completed, cancelled)
- `--priority`: Filter by priority (all, low, medium, high, urgent)
- `--category`: Filter by category (all, personal, work, learning, project)
- `--hide-completed`: Hide completed tasks

**Examples:**
```bash
# List all tasks
python pkms.py task list

# List only high priority pending tasks
python pkms.py task list --priority high --status pending

# List work tasks, hiding completed ones
python pkms.py task list --category work --hide-completed
```

#### Update Task Status

```bash
python pkms.py task update <task_id> <status>
```

**Status Options:** pending, in_progress, completed, cancelled

**Examples:**
```bash
python pkms.py task update 1 in_progress
python pkms.py task update 2 completed
```

#### Quick Complete Task

```bash
python pkms.py task complete <task_id>
```

**Example:**
```bash
python pkms.py task complete 1
```

#### Delete Task

```bash
python pkms.py task delete <task_id>
```

**Example:**
```bash
python pkms.py task delete 1
```

### Note Management

#### Add a Note

```bash
python pkms.py note add "Note title" [options]
```

**Options:**
- `--content, -c`: Note content
- `--category`: Category (personal, work, learning, project)
- `--tags`: Space-separated list of tags
- `--link-tasks`: Space-separated list of task IDs to link

**Examples:**
```bash
python pkms.py note add "Meeting Notes" --content "Discussed project timeline and deliverables" --category work --tags meeting project

python pkms.py note add "Python Tips" --content "Use list comprehensions for better performance" --tags python tips --category learning

python pkms.py note add "Project Ideas" --content "Mobile app for task management" --link-tasks 1 2 --tags ideas mobile
```

#### List Notes

```bash
python pkms.py note list [options]
```

**Options:**
- `--category`: Filter by category (all, personal, work, learning, project)
- `--tag`: Filter by specific tag

**Examples:**
```bash
# List all notes
python pkms.py note list

# List work-related notes
python pkms.py note list --category work

# List notes with 'python' tag
python pkms.py note list --tag python
```

#### View Full Note

```bash
python pkms.py note view <note_id>
```

**Example:**
```bash
python pkms.py note view 1
```

#### Delete Note

```bash
python pkms.py note delete <note_id>
```

**Example:**
```bash
python pkms.py note delete 1
```

### Search and Discovery

#### Search Across All Items

```bash
python pkms.py search "keyword" [options]
```

**Options:**
- `--type`: Search type (all, tasks, notes)

**Examples:**
```bash
# Search for "python" in all items
python pkms.py search "python"

# Search for "meeting" only in notes
python pkms.py search "meeting" --type notes

# Search for "urgent" only in tasks
python pkms.py search "urgent" --type tasks
```

### Analytics and Export

#### View Statistics

```bash
python pkms.py stats
```

Shows comprehensive statistics including:
- Task counts by status
- Overdue tasks
- Note counts
- Categories and tags summary
- Completion rates

#### Export Data

```bash
python pkms.py export [options]
```

**Options:**
- `--format`: Export format (json, markdown)
- `--output`: Output filename

**Examples:**
```bash
# Export as JSON
python pkms.py export --format json

# Export as Markdown with custom filename
python pkms.py export --format markdown --output my_pkms_backup.md
```

## Visual Indicators

### Task Status Icons
- `○` Pending
- `◐` In Progress
- `✓` Completed
- `✗` Cancelled

### Priority Indicators
- 🟢 Low priority
- 🟡 Medium priority
- 🟠 High priority
- 🔴 Urgent priority

### Due Date Warnings
- ⚠️ OVERDUE (past due date)
- 📅 DUE TODAY (due today)
- ⏰ DUE SOON (due within 3 days)

## Data Storage

The PKMS stores data in JSON files within a `data/` directory:

```
tasks2/
├── pkms.py                # Main application
├── data/                  # Data directory (created automatically)
│   ├── tasks.json        # Task storage
│   ├── notes.json        # Note storage
│   └── config.json       # Configuration settings
└── README.md             # This file
```

### Task Data Structure

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "priority": "high",
  "category": "work",
  "due_date": "2025-11-10",
  "tags": ["python", "development"],
  "status": "pending",
  "completed": false,
  "created_at": "2025-11-02 10:30:00",
  "updated_at": "2025-11-02 10:30:00",
  "dependencies": [],
  "notes": []
}
```

### Note Data Structure

```json
{
  "id": 1,
  "title": "Note title",
  "content": "Note content here...",
  "category": "learning",
  "tags": ["python", "tips"],
  "linked_tasks": [1, 2],
  "created_at": "2025-11-02 10:30:00",
  "updated_at": "2025-11-02 10:30:00"
}
```

## Workflow Examples

### Daily Task Management

```bash
# Start your day - check what's pending and urgent
python pkms.py task list --status pending --priority urgent

# Check overdue tasks
python pkms.py stats

# Add a new task for today
python pkms.py task add "Review code" --priority high --due 2025-11-02 --category work

# Start working on a task
python pkms.py task update 1 in_progress

# Complete a task
python pkms.py task complete 1

# Add notes about your work
python pkms.py note add "Code Review Notes" --content "Found potential memory leak in module X" --category work --link-tasks 1
```

### Project Management

```bash
# Create project tasks
python pkms.py task add "Design database schema" --priority high --category project --tags database design
python pkms.py task add "Implement API endpoints" --priority medium --category project --tags api development
python pkms.py task add "Write documentation" --priority low --category project --tags docs

# Track project notes
python pkms.py note add "Architecture Decisions" --content "Using PostgreSQL for main database" --category project --tags architecture database

# Monitor project progress
python pkms.py task list --category project

# Search project-related items
python pkms.py search "database" --type all
```

### Learning and Knowledge Management

```bash
# Track learning goals
python pkms.py task add "Complete Python course" --due 2025-12-01 --category learning --tags python course

# Take notes while learning
python pkms.py note add "Python Decorators" --content "Decorators are functions that modify other functions" --tags python decorators --category learning

# Link notes to learning tasks
python pkms.py note add "Course Progress" --content "Completed modules 1-5" --link-tasks 1 --category learning

# Find all learning materials
python pkms.py search "python" --type all
python pkms.py note list --category learning
```

## Advanced Features

### Batch Operations

You can create shell scripts to perform batch operations:

**Windows PowerShell example:**
```powershell
# Add multiple related tasks
python pkms.py task add "Task 1" --category project --tags sprint1
python pkms.py task add "Task 2" --category project --tags sprint1
python pkms.py task add "Task 3" --category project --tags sprint1
```

### Regular Maintenance

```bash
# Weekly review - check overdue and pending items
python pkms.py stats
python pkms.py task list --status pending

# Monthly backup
python pkms.py export --format json --output monthly_backup_$(date +%Y%m%d).json
```

## Troubleshooting

### Common Issues

1. **"No tasks/notes found"**: You haven't added any items yet. Use the `add` commands to create your first items.

2. **"Task/Note ID not found"**: Make sure you're using the correct ID shown in the list commands.

3. **Python not found**: Use `py` instead of `python` on Windows systems, or ensure Python is in your PATH.

4. **JSON decode error**: The data files may be corrupted. Check the `data/` directory and remove corrupted files to start fresh.

5. **Permission errors**: Ensure you have write permissions in the directory where you're running the application.

### Data Recovery

If data files become corrupted:

1. Check the `data/` directory for backup files
2. Remove corrupted JSON files to start fresh
3. Re-import data from export files if available

### Performance Tips

- Use specific filters when listing large numbers of items
- Regular cleanup of completed/old items
- Use search instead of listing all items when looking for specific content

## Differences from Tasks1

This enhanced PKMS (tasks2) includes several improvements over the basic task manager (tasks1):

### New Features
- **Note management system** with rich content and linking
- **Priority levels** with visual indicators
- **Due date tracking** with overdue warnings  
- **Category system** for better organization
- **Enhanced tagging** across tasks and notes
- **Status tracking** beyond just completed/pending
- **Advanced search** across all content types
- **Export capabilities** in multiple formats
- **Statistics and analytics** dashboard
- **Data relationships** between tasks and notes

### Improved Architecture
- **Modular design** with separate manager classes
- **Better CLI interface** using argparse
- **Enhanced data validation** and error handling
- **Structured data storage** with separate files
- **Configuration management** for customization

### Better User Experience
- **Visual indicators** for status and priority
- **Comprehensive help** with examples
- **Flexible filtering** and sorting options
- **Context-aware search** with result highlighting
- **Batch operation support** for productivity

## License

This is an enhanced prototype application created for educational purposes as part of CSC299 coursework.

## Contributing

This is a learning project. Feel free to extend and modify the code for your own educational purposes.