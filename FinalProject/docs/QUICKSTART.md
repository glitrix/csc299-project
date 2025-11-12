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

3. **Set up OpenAI API key (REQUIRED - Most features use AI!):**
   - See [OPENAI_SETUP.md](OPENAI_SETUP.md) for setup instructions
   - **Required for ALL AI features**: planning, search, suggestions, summaries, quiz, ask, expand

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

### 11. AI Semantic Search (Natural Language!)
```
search notes "what did I learn about loops?"
```
*Uses AI to understand meaning, not just keywords!*

### 12. Get AI Summary
```
summary 1
```
*Get an intelligent summary of your note!*

### 13. AI-Powered Link Suggestions
```
suggest links 1
```
*See why notes should be linked with AI reasoning!*

### 14. AI Tag Suggestions
```
suggest tags 1
```
*Get contextually relevant tag suggestions!*

### 15. Ask Questions About Your Notes
```
ask "What topics should I review for my exam?"
```
*AI assistant answers based on your notes and tasks!*

### 16. Generate Quiz Questions
```
quiz 1 --num 5
```
*AI creates quiz questions to test your understanding!*

### 17. AI-Assisted Note Improvement
```
expand 1 --mode clarify
```
*Modes: expand, clarify, examples, simplify*

### 18. Get Daily AI Recommendations
```
plan today
```

### 19. Generate Weekly AI Study Plan
```
plan week
```

## Complete Command Reference

### 📝 Note Management
| Command | Description | Example |
|---------|-------------|---------|
| `add note "Title"` | Create a note | `add note "Math Notes" --tags math,calculus` |
| `list notes` | Show all notes | `list notes --tag python` |
| `show note <id>` | View note details | `show note 1` |
| `update note <id>` | Modify note | `update note 1 --title "New Title"` |
| `delete note <id>` | Remove note | `delete note 1` |
| `link note <id1> to <id2>` | Link notes | `link note 1 to 2` |

### ✅ Task Management
| Command | Description | Example |
|---------|-------------|---------|
| `add task "Title"` | Create a task | `add task "Study" --priority 5 --due 2025-11-20` |
| `list tasks` | Show tasks | `list tasks --status todo` |
| `show task <id>` | View task | `show task 1` |
| `update task <id>` | Modify task | `update task 1 --status done` |
| `delete task <id>` | Remove task | `delete task 1` |
| `stats` | Task statistics | `stats` |

### 🤖 AI-Powered Features (All require OpenAI API)
| Command | Description | Example |
|---------|-------------|---------|
| `search notes "query"` | Semantic search | `search notes "explain loops"` |
| `suggest links <id>` | AI link suggestions with reasons | `suggest links 1` |
| `suggest tags <id>` | AI tag suggestions | `suggest tags 1` |
| `summary <id>` | AI-generated summary | `summary 1` |
| `ask "question"` | Ask about notes/tasks | `ask "What should I study today?"` |
| `quiz <id>` | Generate quiz questions | `quiz 1 --num 5` |
| `expand <id>` | AI note improvement | `expand 1 --mode examples` |
| `plan week` | Weekly AI study plan | `plan week` |
| `plan today` | Daily AI recommendations | `plan today` |

### 🛠️ General Commands
| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all commands | `help` |
| `exit` or `quit` | Close StudyPal | `exit` |

## AI Features Explained

### 🔍 Semantic Search
Unlike keyword search, semantic search understands **meaning**:
- "show me notes about iteration" → finds notes about loops, for loops, while loops
- "what covers object-oriented programming" → finds OOP, classes, inheritance notes

### 🔗 AI Link Suggestions
AI analyzes note content and suggests conceptual connections:
- Identifies prerequisite knowledge (e.g., "Variables" → "Functions")
- Finds complementary topics (e.g., "Sorting" → "Time Complexity")
- Shows WHY notes should be linked

### 🏷️ AI Tag Suggestions
Context-aware tag generation:
- Analyzes content, not just keywords
- Suggests existing tags when appropriate
- Creates new meaningful tags when needed

### 📊 AI Study Planning
- **Weekly Plan**: Balances workload, considers priorities and deadlines
- **Daily Recommendations**: Top 5 tasks based on urgency and importance

### 💬 Knowledge Assistant (`ask`)
RAG-powered Q&A:
- "What should I study for my exam?" → Reviews your notes and tasks
- "Explain the connection between X and Y" → Analyzes related notes
- "What topics have I covered?" → Summarizes your knowledge base

### 📝 Quiz Generator
Creates test questions from your notes:
- Multiple choice questions
- True/false questions
- Short answer questions
- Tests understanding, not just memorization

### ✨ Note Expansion
AI-assisted content improvement:
- **expand**: Add more detail and explanation
- **clarify**: Improve clarity and understanding
- **examples**: Add practical examples
- **simplify**: Make easier to understand

## Tips

- **Tags**: Use descriptive tags to organize notes (e.g., python, math, algorithms)
- **Priorities**: Use 5 for urgent tasks, 1 for low priority
- **Due Dates**: Format as YYYY-MM-DD (e.g., 2025-11-20)
- **Links**: Connect related notes to build a knowledge graph
- **AI Features**: Use them regularly! They get better with more notes
- **Semantic Search**: Ask natural questions instead of keyword searches
- **Ask Command**: Great for study planning and knowledge discovery

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

## Example Workflows

### 📚 Start of Week
```bash
list tasks                    # Review what needs to be done
plan week                     # AI generates balanced weekly schedule
ask "What are my priorities this week?"  # Get AI insights
```

### 📅 Daily Study Routine
```bash
plan today                    # Get top 5 AI-recommended tasks
show task 1                   # Review task details
add note "Today's Learning"   # Take notes as you study
suggest tags 5                # AI suggests relevant tags
```

### 📖 After Taking Notes
```bash
suggest links 5               # AI finds related notes
link note 5 to 3             # Connect related concepts
summary 5                     # Generate AI summary for review
quiz 5 --num 3               # Test your understanding
```

### 🔍 Finding Information
```bash
search notes "explain recursion"        # Semantic search
ask "What notes cover data structures?" # Ask AI assistant
```

### ✅ Completing Tasks
```bash
update task 1 --status done   # Mark as complete
stats                         # Check your progress
```

### 🎯 Exam Preparation
```bash
ask "What should I review for my exam?"  # Get AI recommendations
list notes --tag exam                    # Find exam-related notes
quiz 1                                   # Generate practice questions
expand 2 --mode examples                 # Add examples to notes
```

### 💡 Improving Your Notes
```bash
summary 3                     # Get concise summary
expand 3 --mode clarify       # AI improves clarity
expand 3 --mode examples      # AI adds examples
expand 3 --mode simplify      # AI simplifies content
```

## Common Patterns

### Adding Comprehensive Notes
```bash
add note "Python Functions" --tags python,programming --content "Functions are reusable blocks of code..."
suggest tags 1                # AI suggests more tags
suggest links 1               # AI finds related notes
```

### Working with Tasks
```bash
add task "Study Chapter 5" --due 2025-11-15 --priority 4 --desc "Focus on algorithms"
list tasks --status todo      # See pending tasks
plan today                    # AI prioritizes for you
```

### Building Knowledge Connections
```bash
suggest links 1               # AI suggests connections
link note 1 to 2             # Create the link
show note 1                   # Verify links created
```

Happy studying! 🚀📚
