# StudyPal Quick Start Guide

## Installation & First Run

1. **Navigate to the FinalProject directory:**
   ```powershell
   cd FinalProject
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key (REQUIRED for planning features):**
   - See [OPENAI_SETUP.md](OPENAI_SETUP.md) for setup instructions
   - Required for `plan week` and `plan today` commands

4. **Verify installation:**
   ```powershell
   py verify.py
   ```
   
   You should see all tests pass with green checkmarks.

5. **Start StudyPal:**
   ```powershell
   py studypal.py
   ```
   
   Or alternatively:
   ```powershell
   py -m src.studypal
   ```

## Your First Session

Try these commands in order to learn StudyPal:

### 1. Create Your First Note
```
add note "Python Basics" --tags python,programming --content "Variables, functions, loops"
```

### 2. Create Another Note
```
add note "Data Structures" --tags python,algorithms
```

### 3. List Your Notes
```
list notes
```

### 4. Create a Task
```
add task "Study Python loops" --due 2025-11-20 --priority 4
```

### 5. List Tasks
```
list tasks
```

### 6. Get AI Suggestions
```
suggest links 1
```

### 7. Link Related Notes
```
link note 1 to 2
```

### 8. View a Note with Links
```
show note 1
```

### 9. Generate a Weekly Study Plan
```
plan week
```
*Note: This uses OpenAI AI for intelligent scheduling! (Requires API key)*

### 10. Get Task Statistics
```
stats
```

### 11. Search Notes
```
search notes "python"
```

### 12. Get Daily Recommendations
```
plan today
```
*Note: This uses OpenAI AI for intelligent prioritization! (Requires API key)*

## Common Commands Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add note "Title"` | Create a note | `add note "Math Notes"` |
| `list notes` | Show all notes | `list notes` |
| `show note <id>` | View note details | `show note 1` |
| `add task "Title"` | Create a task | `add task "Homework"` |
| `list tasks` | Show all tasks | `list tasks` |
| `update task <id>` | Modify a task | `update task 1 --status done` |
| `suggest links <id>` | AI link suggestions | `suggest links 1` |
| `plan week` | Weekly study plan | `plan week` |
| `stats` | Task statistics | `stats` |
| `help` | Show help | `help` |
| `exit` | Quit StudyPal | `exit` |

## Tips

- **Tags**: Use descriptive tags to organize notes (e.g., python, math, algorithms)
- **Priorities**: Use 5 for urgent tasks, 1 for low priority
- **Due Dates**: Format as YYYY-MM-DD (e.g., 2025-11-20)
- **Links**: Connect related notes to build a knowledge graph
- **AI Agents**: Use them regularly to discover connections and plan your study time

## Running Tests

To ensure everything is working correctly:

```powershell
py -m pytest
```

For detailed test output:

```powershell
py -m pytest -v
```

## Data Location

All your notes and tasks are stored in:
```
FinalProject/data/
  ├── notes.json
  └── tasks.json
```

You can backup these files to preserve your data.

## Need Help?

- Type `help` in StudyPal for command reference
- See `README.md` for detailed documentation
- Check `tests/` for usage examples

## Example Workflow

1. **Start of Week:**
   - Review tasks: `list tasks`
   - Generate plan: `plan week`

2. **Daily:**
   - Check today's tasks: `plan today`
   - Add new notes as you study
   - Link related notes

3. **End of Study Session:**
   - Update task status: `update task <id> --status done`
   - Add tags to new notes
   - Check stats: `stats`

Happy studying! 📚
