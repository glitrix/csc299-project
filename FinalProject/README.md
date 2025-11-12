# StudyPal

A terminal-based study assistant that combines Personal Knowledge Management (PKMS), task management, and AI agents to help you organize your studies.

## Features

### 📝 Personal Knowledge Management System (PKMS)
- Create and organize notes in Markdown format
- Tag notes for easy categorization
- Link related notes together
- Full-text search across all notes
- Manage tags and relationships

### ✅ Task Management
- Create tasks with priorities (1-5) and due dates
- Track task status (todo, in_progress, done)
- View overdue and upcoming tasks
- Get task statistics and completion rates

### 🤖 AI Agents
- **Link Suggester**: Automatically suggests related notes based on content similarity
- **Tag Suggester**: Recommends relevant tags based on note content
- **Study Planner**: Generates weekly study plans (enhanced with OpenAI API if configured)
- **Summary Generator**: Creates concise summaries of your notes

**NEW:** Optional OpenAI API integration for enhanced planning features! See [OPENAI_SETUP.md](OPENAI_SETUP.md) for details.

### 💾 Data Storage
- Uses JSON files for simple, portable storage
- All data stored locally in `data/` directory
- Works offline (OpenAI API is optional)

## Installation

### Prerequisites
- Python 3.11 or higher

### Setup

1. Clone or download this repository

2. Navigate to the FinalProject directory:
```powershell
cd FinalProject
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. **(Optional) Enable AI-powered planning:**
   - See [OPENAI_SETUP.md](OPENAI_SETUP.md) for instructions
   - StudyPal works great without an API key!

## Usage

### Starting StudyPal

**Simple method (Windows):**
```powershell
py studypal.py
```

**Or using module execution:**

**On Windows:**
```powershell
py -m src.studypal
```

**On macOS/Linux:**
```bash
python3 -m src.studypal
```

Or with custom data directory:

**Windows:**
```powershell
py -m src.studypal --data-dir "C:\path\to\data"
```

**macOS/Linux:**
```bash
python3 -m src.studypal --data-dir "/path/to/data"
```

### Available Commands

Once StudyPal is running, you'll see a prompt where you can enter commands.

#### Note Commands

```
add note "Title" [--tags tag1,tag2] [--content "content"]
    Create a new note

list notes [--tag tagname]
    List all notes or filter by tag

show note <id>
    Display a specific note with full details

search notes "keyword"
    Search for notes containing a keyword

update note <id> [--title "New Title"] [--content "content"] [--tags tag1,tag2]
    Update an existing note

delete note <id>
    Delete a note

link note <id1> to <id2> [--type related]
    Create a connection between two notes
```

#### Task Commands

```
add task "Title" [--due YYYY-MM-DD] [--priority 1-5] [--desc "description"]
    Create a new task

list tasks [--status todo|in_progress|done] [--priority 1-5]
    List all tasks or filter by status/priority

show task <id>
    Display a specific task with full details

update task <id> [--title "New Title"] [--status done] [--priority 4]
    Update an existing task

delete task <id>
    Delete a task

stats
    Show task statistics (completion rate, overdue, etc.)
```

#### AI Agent Commands

```
suggest links <note_id>
    Get suggestions for related notes based on content similarity

suggest tags <note_id>
    Get tag suggestions for a note

plan week
    Generate a weekly study plan based on your tasks

plan today
    Get recommended tasks to work on today

summary <note_id>
    Generate a summary of a note
```

#### General Commands

```
help
    Display help information

exit or quit
    Close StudyPal
```

## Example Session

```
$ py -m src.studypal
Welcome to StudyPal!
Type 'help' for available commands or 'exit' to quit.

studypal> add note "Python Basics" --tags python,programming --content "Variables, functions, and control flow"
Created note #1: Python Basics
Tags: python, programming

studypal> add note "Object-Oriented Programming" --tags python,oop
Created note #2: Object-Oriented Programming

studypal> add task "Study Python loops" --due 2025-11-20 --priority 4
Created task #1: Study Python loops
Due: 2025-11-20
Priority: 4

studypal> list notes
Found 2 note(s):
----------------------------------------------------------------------
#1: Python Basics [python, programming]
    Variables, functions, and control flow
#2: Object-Oriented Programming [python, oop]
----------------------------------------------------------------------

studypal> suggest links 1
Suggested links for note #1:
----------------------------------------------------------------------
#2: Object-Oriented Programming (similarity: 0.35)
----------------------------------------------------------------------

studypal> link note 1 to 2
Linked note #1 to note #2 (related)

studypal> plan week
Weekly Study Plan:
======================================================================

Monday:
  • Study Python loops (2h) [P4]

Tuesday:
  • Review: Python Basics (0.5h)

...

studypal> stats
Task Statistics:
======================================================================
Total tasks: 1
  • To do: 1
  • In progress: 0
  • Completed: 0

Overdue: 0
Due this week: 1
Completion rate: 0.0%
======================================================================

studypal> exit
Goodbye!
```

## Project Structure

```
FinalProject/
├── src/studypal/          # Main application code
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Entry point
│   ├── cli.py             # Command-line interface
│   ├── pkms.py            # Personal Knowledge Management System
│   ├── tasks.py           # Task management
│   ├── agents.py          # AI agents
│   ├── storage.py         # JSON storage layer
│   └── utils.py           # Helper utilities
│
├── tests/                 # Test files
│   ├── test_pkms.py       # PKMS tests
│   ├── test_tasks.py      # Task management tests
│   ├── test_agents.py     # AI agent tests
│   └── test_inc.py        # Basic tests
│
├── data/                  # Data storage (JSON files)
│   ├── notes.json         # Notes storage
│   └── tasks.json         # Tasks storage
│
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── pytest.ini             # Test configuration
└── README.md              # This file
```

## Testing

Run tests using pytest:

**Windows:**
```powershell
py -m pytest
```

**macOS/Linux:**
```bash
python3 -m pytest
```

Run tests with verbose output:

```powershell
py -m pytest -v
```

Run specific test file:

```powershell
py -m pytest tests/test_pkms.py
```

## Development

### Running Tests During Development

```powershell
# Run all tests
py -m pytest

# Run with coverage (requires pytest-cov)
py -m pytest --cov=src.studypal

# Run specific test
py -m pytest tests/test_pkms.py::test_add_note -v
```

### Code Organization

- **storage.py**: Low-level JSON file operations
- **pkms.py**: Note management and PKMS features
- **tasks.py**: Task creation, updates, and queries
- **agents.py**: AI-powered analysis and suggestions
- **cli.py**: Command parsing and user interface
- **utils.py**: Helper functions used across modules

## Technical Details

### Cross-Platform Compatibility
- Uses `pathlib` for file paths (works on Windows, macOS, Linux)
- JSON storage is platform-independent
- No OS-specific dependencies

### Data Storage Format

Notes are stored in `data/notes.json`:
```json
{
  "notes": [
    {
      "id": 1,
      "title": "Note Title",
      "content": "Note content...",
      "tags": ["tag1", "tag2"],
      "created_at": "2025-11-12T10:00:00",
      "updated_at": "2025-11-12T10:00:00"
    }
  ],
  "links": [
    {
      "from_note_id": 1,
      "to_note_id": 2,
      "link_type": "related"
    }
  ],
  "next_id": 2
}
```

Tasks are stored in `data/tasks.json`:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Description...",
      "status": "todo",
      "priority": 3,
      "due_date": "2025-11-20",
      "created_at": "2025-11-12T10:00:00",
      "updated_at": "2025-11-12T10:00:00"
    }
  ],
  "next_id": 2
}
```

## AI Agent Details

### Link Suggester
- Analyzes note content using keyword extraction
- Calculates similarity using Jaccard index
- Considers shared tags for additional similarity boost
- Excludes already-linked notes from suggestions

### Tag Suggester
- Extracts keywords from note content
- Matches against existing tags in the system
- Suggests tags that appear in the note but aren't currently assigned

### Study Planner
- Prioritizes tasks by due date and priority level
- Distributes tasks across the week
- Includes review time for existing notes
- Estimates time based on task priority

### Summary Generator
- Extracts key sentences from note content
- Uses simple extractive summarization
- Returns first, middle, and last sentences for longer notes

## Contributing

This is a student project for CSC299. See SUMMARY.md for development process documentation.

## License

Educational project - CSC299 Final Project

## Author

Created as part of CSC299 coursework
