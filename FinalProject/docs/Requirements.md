# StudyPal Requirements

A terminal-based study assistant combining a **Personal Knowledge Management System (PKMS)**, **task management**, a **chat interface**, and **AI agents** for study assistance.

> **Core constraint:** Python-only project. Must run portably on Windows, macOS, and Linux.

---

## 1) Goals & Scope

### Core Features
- **PKMS:** Store and organize study notes (Markdown format) with tags and links between notes
- **Task Management:** Create and track tasks with due dates, priorities, and status tracking
- **Chat Interface:** Terminal-based command interface for interacting with notes and tasks
- **AI Agents:** Automated helpers that work with your stored knowledge and tasks

### Data Storage
- **Primary:** SQLite database (recommended for final version)
- **Alternative:** JSON files (suitable for prototypes and development)
- **Neo4J:** Optional for advanced graph-based relationships

### Design Principles
- Keep it simple and usable
- Work offline by default
- Easy to test and maintain
- Clear command structure

**What's NOT included:** Web interfaces, cloud sync, multi-user support

---

## 2) Requirements & Constraints

### Technical Requirements
- **Language:** Python 3.11+ only
- **Cross-Platform:** Must work on Windows, macOS, and Linux
  - Use `pathlib` for file paths (not string concatenation)
  - Use `os` or `platform` modules for OS-specific needs
- **State Storage:** 
  - SQLite (recommended for production)
  - JSON files (acceptable, especially for prototypes)
  - Neo4J (optional advanced feature)

### Development Requirements  
- **Dependencies:** Keep minimal and well-documented in `requirements.txt`
- **Testing:** Use `pytest` for automated tests
- **Entry Point:** Simple command to start the program (e.g., `python -m studypal` or `studypal`)
- **Git History:** Fine-grained commits showing development progression

### User Experience
- **Offline First:** Core features work without internet connection
- **Clear Commands:** Easy-to-remember terminal commands
- **Helpful Feedback:** Show what's happening and any errors clearly

---

## 3) Suggested Project Structure

Here's a flexible structure - adapt it to your needs:

```
/studypal/
  ├─ src/studypal/          # Main application code
  │   ├─ __main__.py        # Entry point for running program
  │   ├─ cli.py             # Command-line interface and chat loop
  │   ├─ pkms.py            # PKMS functionality (notes, tags, links)
  │   ├─ tasks.py           # Task management
  │   ├─ agents.py          # AI agent implementations
  │   ├─ storage.py         # Database/file operations
  │   └─ utils.py           # Helper functions
  │
  ├─ tests/                 # Test files
  │   ├─ test_pkms.py
  │   ├─ test_tasks.py
  │   └─ test_agents.py
  │
  ├─ prototypes/            # Earlier explorations (keep for documentation)
  ├─ data/                  # Storage for JSON files or SQLite database
  ├─ README.md              # Project overview and setup instructions
  ├─ SUMMARY.md             # Development process documentation (REQUIRED)
  ├─ video.txt              # YouTube URL to demo video (REQUIRED)
  ├─ requirements.txt       # Python dependencies
  └─ pyproject.toml         # Optional: for packaging
```

**Note:** This is a suggestion. Organize your code in a way that makes sense to you. The important parts are:
- Clear separation of concerns
- Easy to find and test components
- Include required files (README.md, SUMMARY.md, video.txt)

---

## 4) Data Models

### SQLite Schema (Recommended)

If using SQLite, here's a simple schema to get started:

```sql
-- Notes/Knowledge Base
CREATE TABLE notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  tags TEXT,                    -- Comma-separated or JSON array
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Links between notes
CREATE TABLE links (
  from_note_id INTEGER,
  to_note_id INTEGER,
  link_type TEXT DEFAULT 'related',
  FOREIGN KEY (from_note_id) REFERENCES notes(id),
  FOREIGN KEY (to_note_id) REFERENCES notes(id)
);

-- Tasks
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'todo',   -- todo, in_progress, done
  priority INTEGER DEFAULT 2,    -- 1 (low) to 5 (high)
  due_date TEXT,                -- YYYY-MM-DD format
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### JSON File Format (Alternative)

For JSON storage, use simple structures:

```json
{
  "notes": [
    {
      "id": 1,
      "title": "Python Basics",
      "content": "# Python Basics\n\n...",
      "tags": ["programming", "python"],
      "created_at": "2025-11-12T10:00:00",
      "updated_at": "2025-11-12T10:00:00"
    }
  ],
  "tasks": [
    {
      "id": 1,
      "title": "Complete homework",
      "status": "todo",
      "priority": 3,
      "due_date": "2025-11-20",
      "created_at": "2025-11-12T10:00:00"
    }
  ]
}
```

**Choose the format that works best for your implementation.**

---

## 5) Example Python Data Structures

Here are simple Python classes you might use (adapt as needed):

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Note:
    """Represents a knowledge note"""
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    tags: List[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class Task:
    """Represents a task to complete"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    status: str = "todo"  # todo, in_progress, done
    priority: int = 2  # 1-5, where 5 is highest
    due_date: Optional[str] = None  # YYYY-MM-DD format
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

**Note:** Use simple dictionaries if you prefer - dataclasses are just one option.
---

## 6) Terminal Chat Interface

Your program should provide a command-line interface where users type commands and see results.

### Basic Command Examples

Start simple and expand as needed:

**PKMS Commands:**
- `add note "Title" --tags tag1,tag2` - Create a new note
- `list notes` - Show all notes
- `show note <id>` - Display a specific note
- `search notes "keyword"` - Find notes containing text
- `link note <id1> to <id2>` - Create connection between notes

**Task Commands:**
- `add task "Task name" --due 2025-11-20 --priority 3` - Create task
- `list tasks` - Show all tasks
- `update task <id> --status done` - Update task status
- `show task <id>` - Display task details
- `tasks due` - Show tasks with upcoming due dates

**AI Agent Commands:**
- `suggest links for note <id>` - AI suggests related notes
- `generate summary of note <id>` - AI creates summary
- `plan week` - AI suggests weekly schedule based on tasks

**General:**
- `help` - Show available commands
- `exit` or `quit` - Close the program

### Interface Design Tips

1. **Keep it simple:** Start with basic commands that work
2. **Be forgiving:** Accept variations (e.g., "quit" and "exit")
3. **Give feedback:** Always tell users what happened
4. **Handle errors gracefully:** Explain what went wrong and how to fix it
5. **Consider a loop structure:**
   ```python
   while True:
       command = input("studypal> ")
       if command in ["exit", "quit"]:
           break
       process_command(command)
   ```

---

## 7) AI Agents

AI agents should interact with your stored knowledge and tasks. Here are some ideas - implement what makes sense for your project:

### Agent Ideas

**1. Link Suggester**
- Analyzes note content and suggests connections to other notes
- Simple approach: Find notes with similar keywords or tags
- Advanced: Use word frequency analysis (TF-IDF) to find related content
- Example: "Note about 'Python loops' might link to 'Control flow' note"

**2. Study Planner**
- Looks at your tasks and suggests a study schedule
- Consider: due dates, priorities, estimated time
- Output: Suggested daily/weekly plan
- Example: "Monday: Work on Math homework (2 hours), Review Python notes (30 min)"

**3. Summary Generator**
- Creates concise summaries of notes
- Could use simple text extraction or LLM if available
- Helpful for quick review

**4. Tag Suggester**
- Recommends tags for notes based on content
- Look at common words, compare to existing tags
- Helps maintain consistent tagging

### Implementation Approaches

**Simple (Rule-Based):**
- Use keyword matching
- Count word frequencies
- Simple text analysis with Python's built-in tools

**Advanced (with AI APIs):**
- Use OpenAI API for intelligent suggestions
- Make it optional - work offline by default
- Store API key as environment variable
- Example:
  ```python
  import os
  if os.getenv("OPENAI_API_KEY"):
      # Use AI features
  else:
      # Use simple rule-based approach
  ```

**Important:** Your agents should actually DO something useful, not just display information. They should analyze, suggest, or help organize your data.

---

## 8) Testing & Development

### Testing with pytest
- Write tests for your main functionality
- Test note creation, retrieval, and search
- Test task management features  
- Test AI agent functions with sample data
- Run tests with: `pytest` or `python -m pytest`

### Development Tips
1. **Start with prototypes:** Create simple JSON-based versions first
2. **Iterate gradually:** Add features one at a time
3. **Commit often:** Make fine-grained commits showing your progress
4. **Test as you go:** Don't wait until the end to test
5. **Document your process:** Keep notes for your SUMMARY.md

---

## 9) Configuration & Setup

### File Storage
Keep your data files organized:
- Default location: `./data/` or `~/.studypal/`
- For SQLite: `studypal.db`
- For JSON: `notes.json`, `tasks.json`

### Environment Variables (Optional)
```python
import os

# For AI features (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Custom data directory
DATA_DIR = os.getenv("STUDYPAL_DATA", "./data")
```

### Command-Line Arguments
Consider adding flags for flexibility:
- `--data-dir PATH` - Custom data directory
- `--db PATH` - Custom database path (useful for testing)
- `--help` - Show available commands

---

## 10) Project Deliverables (REQUIRED)

Make sure your repository includes:

### 1. Working Software
- Python code that runs on Windows, macOS, and Linux
- Clear entry point (how to start the program)
- All features implemented and functional

### 2. README.md
- Project overview
- Installation instructions
- How to run the program
- Example commands
- List of features

### 3. SUMMARY.md (CRITICAL)
This should be detailed (500+ words recommended) and explain:
- **How you used AI-coding assistants:**
  - GitHub Copilot (autocomplete, chat, inline suggestions?)
  - ChatGPT or Claude (planning, debugging, code generation?)
  - Any other AI tools
- **Your development process:**
  - How you planned the project
  - How you created specifications
  - How you developed and tested
  - How you iterated and improved
- **What worked well:**
  - Which AI tools/techniques were most helpful?
  - What processes led to success?
- **What didn't work:**
  - False starts or mistakes
  - Times when AI suggestions were wrong
  - What you had to do manually
- **Specific examples and details**

### 4. video.txt
- Contains single YouTube URL
- 6-8 minute video demonstrating:
  - Your software running
  - Key features in action
  - Overview of development process
  - Brief code walkthrough

### 5. Fine-Grained Commit History
- Show incremental development
- Don't just commit everything at the end
- Commits should show: specs → prototypes → tests → implementation → refinements

### 6. Tests
- pytest test files
- Tests for main functionality
- Show they pass

---

## 11) Example Session

Here's what using your program might look like:

```
$ python -m studypal
Welcome to StudyPal!
Type 'help' for available commands.

studypal> add note "Python Functions"
Created note #1: Python Functions

studypal> add note "Object-Oriented Programming" --tags python,oop
Created note #2: Object-Oriented Programming

studypal> add task "Complete Python assignment" --due 2025-11-20 --priority 4
Created task #1: Complete Python assignment

studypal> list tasks
Tasks:
1. [Priority 4] Complete Python assignment (due: 2025-11-20) [todo]

studypal> suggest links for note 1
Analyzing note #1...
Suggested links:
- Note #2: Object-Oriented Programming (similarity: 0.75)

studypal> plan week
Weekly Study Plan:
Monday: Complete Python assignment (2 hours)
Tuesday: Review Python Functions note (30 min)
...

studypal> help
Available commands:
  add note <title> [--tags tags]
  list notes
  search notes <query>
  add task <title> [--due date] [--priority 1-5]
  list tasks
  suggest links for note <id>
  plan week
  help
  exit

studypal> exit
Goodbye!
```

---

## 12) Tips for Success

### Use AI Assistants Effectively
- **Plan first:** Describe what you want before coding
- **Iterate:** Start simple, add complexity gradually
- **Review AI suggestions:** Don't blindly accept code
- **Ask for explanations:** Understand what the code does
- **Use for multiple purposes:** Planning, coding, debugging, testing, documentation

### Development Approach
1. **Create simple prototype** (JSON files, basic commands)
2. **Add core features** (PKMS, tasks)
3. **Implement chat interface**
4. **Add AI agents**
5. **Write tests**
6. **Refine and polish**
7. **Move to SQLite if desired**

### Common Pitfalls to Avoid
- Waiting too long to test
- Making everything perfect before committing
- Not documenting your AI assistant usage
- Forgetting to make commits showing progression
- Not testing cross-platform compatibility

---

## 13) Additional Feature Ideas (Optional)

If you finish early, consider adding:
- Export notes to Markdown files
- Import notes from a directory
- Task categories or projects
- Statistics (note count, completion rates)
- Color-coded output
- Search with filters
- Bulk operations
- Backup/restore functionality

---

## Remember

This is YOUR project. These requirements are guidelines - adapt them to create something useful and interesting. Focus on:
- Making it work properly
- Using AI assistants effectively
- Documenting your process thoroughly
- Creating clear commit history
- Having fun building something cool!

---

