# Task Manager - Technical Specification

## System Overview

The Task Manager is a Python-based application that provides comprehensive task management capabilities with JSON-based persistence. The system consists of four primary modules organized in a layered architecture.

## Architecture

### System Layers

```
┌─────────────────────────────────────┐
│     Presentation Layer (CLI)        │
│         cli.py                      │
├─────────────────────────────────────┤
│     Business Logic Layer            │
│         task_manager.py             │
├─────────────────────────────────────┤
│     Data Model Layer                │
│         task.py                     │
├─────────────────────────────────────┤
│     Persistence Layer               │
│         storage.py                  │
└─────────────────────────────────────┘
```

### Module Specifications

## 1. Task Module (`task.py`)

### Class: Task

**Purpose**: Represents a single task entity with all associated properties and behaviors.

#### Properties

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `id` | str | Yes | Auto-generated | Unique identifier (timestamp-based) |
| `title` | str | Yes | - | Task name/summary |
| `description` | str | No | "" | Detailed task description |
| `status` | str | No | "pending" | Current state (pending/in-progress/completed) |
| `created_at` | str | Yes | Now | ISO 8601 timestamp of creation |
| `updated_at` | str | Yes | Now | ISO 8601 timestamp of last update |

#### Methods

##### `__init__(title, description="", status="pending", task_id=None, created_at=None, updated_at=None)`
Initializes a new Task instance.

**Parameters:**
- `title` (str): Required task title
- `description` (str): Optional description
- `status` (str): Initial status
- `task_id` (str): Optional custom ID (auto-generated if None)
- `created_at` (str): Optional creation timestamp (current time if None)
- `updated_at` (str): Optional update timestamp (current time if None)

**Returns:** Task instance

##### `_generate_id() -> str` (static)
Generates a unique task ID using timestamp with microseconds.

**Returns:** Unique ID string in format `YYYYMMDDHHMMSSSSSSSS`

##### `to_dict() -> dict`
Converts task to dictionary for JSON serialization.

**Returns:** Dictionary containing all task properties

**Example:**
```python
{
    "id": "20231115143022123456",
    "title": "Complete report",
    "description": "Write quarterly report",
    "status": "in-progress",
    "created_at": "2023-11-15T14:30:22.123456",
    "updated_at": "2023-11-15T14:30:22.123456"
}
```

##### `from_dict(data: dict) -> Task` (classmethod)
Creates Task instance from dictionary.

**Parameters:**
- `data` (dict): Dictionary with task properties

**Returns:** New Task instance

##### `update_timestamp()`
Updates the `updated_at` field to current time.

**Side Effects:** Modifies `updated_at` property

##### `__repr__() -> str`
Returns developer-friendly string representation.

**Returns:** String like `Task(id=123, title='Do something', status='pending')`

##### `__str__() -> str`
Returns user-friendly string representation.

**Returns:** String like `[PENDING] Do something`

## 2. Storage Module (`storage.py`)

### Class: JSONStorage

**Purpose**: Handles all file I/O operations for task persistence.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `filepath` | Path | Path object pointing to JSON storage file |

#### Methods

##### `__init__(filepath: str = "tasks.json")`
Initializes storage handler.

**Parameters:**
- `filepath` (str): Path to JSON file (relative or absolute)

**Side Effects:** Creates file and parent directories if they don't exist

##### `_ensure_file_exists()`
Creates empty JSON file with empty array if file doesn't exist.

**Side Effects:** Creates file and directories

##### `_read_data() -> List[Dict[str, Any]]`
Reads and parses JSON data from file.

**Returns:** List of task dictionaries

**Error Handling:**
- Returns empty list on JSON decode errors
- Returns empty list on file read errors
- Prints warning message to console

##### `_write_data(data: List[Dict[str, Any]])`
Writes task data to JSON file.

**Parameters:**
- `data` (list): List of task dictionaries to write

**Format:**
- UTF-8 encoding
- 2-space indentation
- Non-ASCII characters preserved

**Raises:** Re-raises exceptions after logging

##### `load_tasks() -> List[Dict[str, Any]]`
Public method to load tasks.

**Returns:** List of task dictionaries

##### `save_tasks(tasks: List[Dict[str, Any]])`
Public method to save tasks.

**Parameters:**
- `tasks` (list): List of task dictionaries

##### `backup(backup_path: str = None)`
Creates backup copy of task file.

**Parameters:**
- `backup_path` (str): Optional custom backup location (defaults to `<filepath>.backup`)

**Side Effects:** Creates backup file

## 3. Task Manager Module (`task_manager.py`)

### Class: TaskManager

**Purpose**: Orchestrates all task operations and business logic.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `storage` | JSONStorage | Storage handler instance |
| `tasks` | List[Task] | In-memory list of all tasks |

#### Methods

##### `__init__(storage_file: str = "tasks.json")`
Initializes task manager.

**Parameters:**
- `storage_file` (str): Path to JSON storage file

**Side Effects:** Loads existing tasks from storage

##### `load_tasks()`
Loads tasks from storage into memory.

**Side Effects:** Populates `self.tasks` list

##### `save_tasks()`
Saves all tasks to storage.

**Side Effects:** Writes to JSON file

##### `create_task(title: str, description: str = "", status: str = "pending") -> Task`
Creates a new task.

**Parameters:**
- `title` (str): Required task title
- `description` (str): Optional description
- `status` (str): Initial status

**Returns:** Newly created Task instance

**Side Effects:**
- Adds task to in-memory list
- Saves to storage

##### `get_task(task_id: str) -> Optional[Task]`
Retrieves task by ID.

**Parameters:**
- `task_id` (str): Task identifier

**Returns:** Task instance or None if not found

**Time Complexity:** O(n) linear search

##### `get_all_tasks() -> List[Task]`
Returns all tasks.

**Returns:** Copy of tasks list

**Note:** Returns a copy to prevent external modification

##### `get_tasks_by_status(status: str) -> List[Task]`
Filters tasks by status.

**Parameters:**
- `status` (str): Status to filter by

**Returns:** List of tasks matching status

**Time Complexity:** O(n) linear search

##### `update_task(task_id: str, title: str = None, description: str = None, status: str = None) -> bool`
Updates task properties.

**Parameters:**
- `task_id` (str): Task to update
- `title` (str): Optional new title
- `description` (str): Optional new description
- `status` (str): Optional new status

**Returns:** True if updated, False if task not found

**Side Effects:**
- Updates task in memory
- Updates timestamp
- Saves to storage

**Note:** Only provided parameters are updated (partial updates supported)

##### `delete_task(task_id: str) -> bool`
Deletes a task.

**Parameters:**
- `task_id` (str): Task to delete

**Returns:** True if deleted, False if not found

**Side Effects:**
- Removes from in-memory list
- Saves to storage

##### `search_tasks(query: str) -> List[Task]`
Searches tasks by keyword.

**Parameters:**
- `query` (str): Search string

**Returns:** List of matching tasks

**Algorithm:** Case-insensitive substring matching on title and description

**Time Complexity:** O(n) linear search

##### `clear_completed_tasks() -> int`
Removes all completed tasks.

**Returns:** Number of tasks removed

**Side Effects:**
- Modifies in-memory list
- Saves to storage if any removed

##### `get_statistics() -> dict`
Calculates task statistics.

**Returns:** Dictionary with keys:
- `total` (int): Total task count
- `pending` (int): Count of pending tasks
- `in_progress` (int): Count of in-progress tasks
- `completed` (int): Count of completed tasks

## 4. CLI Module (`cli.py`)

### Class: TaskManagerCLI

**Purpose**: Provides interactive command-line interface.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `manager` | TaskManager | Task manager instance |
| `commands` | dict | Maps command names to handler methods |

#### Methods

##### `__init__()`
Initializes CLI.

**Side Effects:** Creates TaskManager with default storage

##### `run()`
Starts the interactive REPL loop.

**Behavior:**
- Displays welcome banner
- Reads commands in loop
- Dispatches to appropriate handlers
- Handles KeyboardInterrupt for clean exit

**Format:** `command [arguments]`

##### Command Handlers

All command handlers follow the signature: `handler(args: str) -> None`

###### `add_task(args: str)`
Creates new task interactively.

**Arguments:** Task title (required)

**Prompts for:**
- Description (optional)
- Status (optional, default: pending)

**Output:** Success message with task ID

###### `list_tasks(args: str)`
Lists tasks.

**Arguments:** Status filter (optional)

**Output:** Formatted table of tasks with status and title

###### `view_task(args: str)`
Shows detailed task information.

**Arguments:** Task ID (required)

**Output:** Formatted display of all task properties

###### `update_task(args: str)`
Updates existing task.

**Arguments:** Task ID (required)

**Prompts for:**
- New title (optional)
- New description (optional)
- New status (optional)

**Note:** Leaving prompt blank keeps current value

###### `delete_task(args: str)`
Deletes a task.

**Arguments:** Task ID (required)

**Confirmation:** Requires "yes" to confirm

**Output:** Success or cancellation message

###### `complete_task(args: str)`
Marks task as completed.

**Arguments:** Task ID (required)

**Behavior:** Shortcut for updating status to "completed"

###### `search_tasks(args: str)`
Searches for tasks.

**Arguments:** Search query (required)

**Output:** List of matching tasks

###### `show_statistics(args: str)`
Displays task statistics.

**Arguments:** None

**Output:** Formatted statistics table

###### `clear_completed(args: str)`
Removes completed tasks.

**Arguments:** None

**Confirmation:** Requires "yes" to confirm

**Output:** Count of removed tasks

###### `show_help(args: str)`
Shows command help.

**Arguments:** None

**Output:** Formatted command reference

###### `exit_app(args: str)`
Exits application.

**Arguments:** None

**Behavior:** Calls `sys.exit(0)`

## Data Formats

### JSON Storage Format

```json
[
  {
    "id": "20231115143022123456",
    "title": "Complete project",
    "description": "Finish the task manager application",
    "status": "in-progress",
    "created_at": "2023-11-15T14:30:22.123456",
    "updated_at": "2023-11-15T14:35:10.654321"
  },
  {
    "id": "20231115143025789012",
    "title": "Review documentation",
    "description": "",
    "status": "pending",
    "created_at": "2023-11-15T14:30:25.789012",
    "updated_at": "2023-11-15T14:30:25.789012"
  }
]
```

### Timestamp Format
ISO 8601: `YYYY-MM-DDTHH:MM:SS.ffffff`

Example: `2023-11-15T14:30:22.123456`

## Error Handling

### Storage Errors
- **File Not Found**: Auto-creates file
- **JSON Decode Error**: Returns empty list, logs warning
- **Write Error**: Re-raises after logging

### Business Logic Errors
- **Task Not Found**: Returns None or False
- **Invalid Input**: Returns False or empty list

### CLI Errors
- **Missing Arguments**: Shows usage message
- **Invalid Command**: Shows error with help suggestion
- **KeyboardInterrupt**: Graceful exit with goodbye message
- **General Exceptions**: Caught and displayed to user

## Performance Characteristics

### Time Complexity
- Create task: O(1) plus file write
- Get by ID: O(n) linear search
- Get all: O(1) returns list copy
- Filter by status: O(n) linear search
- Update: O(n) search + file write
- Delete: O(n) search + file write
- Search: O(n) linear search
- Clear completed: O(n) filter + file write

### Space Complexity
- Memory usage: O(n) where n is number of tasks
- All tasks loaded in memory
- JSON file size: ~200-300 bytes per task (depends on content)

### Scalability Limits
- Practical limit: ~10,000 tasks
- Above 10,000: Consider database backend
- File operations become slower with large files
- In-memory operations remain fast

## Security Considerations

### File Access
- No authentication/authorization
- Single-user assumption
- File permissions rely on OS

### Input Validation
- No SQL injection risk (no SQL)
- No XSS risk (no web interface)
- Basic input sanitization in CLI

### Data Privacy
- Plain text storage
- No encryption
- Not suitable for sensitive information

## Extensibility Points

### Adding New Commands
1. Add method to TaskManagerCLI class
2. Add entry to `self.commands` dict
3. Update help text

### Adding Task Properties
1. Add property to Task class `__init__`
2. Update `to_dict()` and `from_dict()`
3. Update TaskManager methods as needed
4. Update CLI prompts/displays

### Custom Storage Backends
1. Create class implementing storage interface
2. Implement `load_tasks()` and `save_tasks()`
3. Pass to TaskManager constructor

### Alternative Interfaces
1. Import TaskManager class
2. Build new interface (web, GUI, API)
3. Use existing business logic

## Testing Recommendations

### Unit Tests
- Task serialization/deserialization
- Storage read/write operations
- TaskManager CRUD operations
- Search and filter logic

### Integration Tests
- Full workflow tests (create, update, delete)
- CLI command tests
- Storage persistence tests

### Edge Cases
- Empty task lists
- Corrupted JSON files
- Very long titles/descriptions
- Special characters in text
- Concurrent access attempts
