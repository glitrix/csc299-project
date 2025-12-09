# Tasks3 - PKMS with Testing

This is the tasks3 implementation of the Personal Knowledge Management System (PKMS) with comprehensive testing using pytest.

## Features

- **Task Management**: Add, complete, delete, and list tasks with priorities
- **Note Management**: Add and manage notes
- **Search Functionality**: Search tasks by keywords
- **Statistics**: Get task statistics and overview
- **Data Persistence**: JSON-based data storage
- **Comprehensive Testing**: 16 test cases covering all core functionality

## Installation and Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management.

1. Install uv (if not already installed):
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. The project is already initialized with:
   ```bash
   uv init tasks3 --name tasks3 --package --vcs none
   uv add --dev pytest
   ```

## Usage

### Running the Application

```bash
uv run tasks3
```

This will run the main demonstration showing:
- Sample tasks with different priorities
- Sample notes
- Task statistics

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_pkms.py -v
```

## Test Coverage

The project includes 16 comprehensive tests covering:

1. **Basic Functionality Tests**:
   - `test_inc()` - Tests the simple increment function
   - `test_add_task_valid()` - Valid task creation
   - `test_add_note_valid()` - Valid note creation

2. **Error Handling Tests**:
   - `test_add_task_invalid_priority()` - Invalid priority handling
   - `test_add_task_empty_title()` - Empty title validation
   - `test_add_note_empty_title()` - Note title validation

3. **Task Management Tests**:
   - `test_complete_task()` - Task completion
   - `test_complete_nonexistent_task()` - Error handling for non-existent tasks
   - `test_delete_task()` - Task deletion
   - `test_delete_nonexistent_task()` - Error handling for deletion

4. **Data Operations Tests**:
   - `test_list_tasks_all()` - Listing all tasks
   - `test_list_tasks_by_status()` - Filtering tasks by status
   - `test_search_tasks()` - Keyword search functionality
   - `test_task_stats()` - Statistics calculation

5. **System Tests**:
   - `test_generate_id_increments()` - ID generation
   - `test_data_persistence()` - Data persistence across instances

## Core Components

### PKMSCore Class

The main class providing:
- Task management (add, complete, delete, list, search)
- Note management (add, list)
- Data persistence (JSON files)
- Statistics and reporting

### Test Infrastructure

- Uses pytest fixtures for isolated testing
- Temporary directories for test data
- Comprehensive error condition testing
- Data persistence validation

## Files Structure

```
tasks3/
├── src/tasks3/
│   ├── __init__.py     # Main entry point with inc() function
│   └── pkms.py         # Core PKMS functionality
├── tests/
│   ├── test_inc.py     # Test for inc() function
│   └── test_pkms.py    # Comprehensive PKMS tests
├── data/               # Data storage (created at runtime)
│   ├── tasks.json      # Task data
│   └── notes.json      # Note data
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Test Results

All 16 tests pass successfully:
- 1 test for the `inc()` function
- 15 tests for PKMS functionality
- 100% test success rate
- Comprehensive coverage of all core features

The implementation successfully meets all requirements:
✅ uv package manager installed and configured  
✅ pytest dependency added  
✅ `inc()` function implemented and tested  
✅ PKMS functionality ported from tasks2  
✅ Comprehensive test suite with 16 tests  
✅ Main method callable via `uv run tasks3`  
✅ All tests passing  
