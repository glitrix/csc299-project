# CSC299 Project

This repository contains coursework for CSC299, including progressive task implementations (tasks1-5) and the final project.

---

## 🎓 FinalProject - StudyPal

**StudyPal** is an intelligent, terminal-based study assistant that combines Personal Knowledge Management (PKMS), task management, and powerful AI agents to create a comprehensive learning companion. Built with Python and powered by OpenAI's GPT-4o-mini, StudyPal helps students organize their studies, manage their workload, and learn more effectively through AI-powered features.

### ✨ Core Features

#### 📝 Personal Knowledge Management System (PKMS)
- **Note Creation & Organization**: Create notes in Markdown format with rich content support
- **Tagging System**: Categorize notes with multiple tags for easy organization
- **Note Linking**: Connect related notes to build a knowledge graph
- **Full-Text Search**: Search notes by keywords in title, content, or tags
- **Tag Management**: View all tags and filter notes by specific tags

#### ✅ Task Management
- **Task Creation**: Create tasks with titles, descriptions, priorities (1-5), and due dates
- **Status Tracking**: Track tasks through three states: `todo`, `in_progress`, and `done`
- **Filtering & Organization**: Filter tasks by status or priority level
- **Due Date Management**: Set and track task deadlines in YYYY-MM-DD format
- **Task Statistics**: View completion rates, overdue tasks, and upcoming deadlines

#### 🤖 AI-Powered Features (All powered by OpenAI GPT-4o-mini)

**Intelligent Note Management:**
- **AI Summary Generator**: Creates intelligent, abstractive summaries of your notes for quick review
- **Semantic Link Suggester**: Analyzes note content to find conceptual relationships and suggests meaningful connections between notes
- **AI Tag Suggester**: Generates contextually relevant tags based on note content using natural language understanding
- **Semantic Search**: Natural language search that finds notes by meaning, not just keywords - understands context and intent

**Study Assistance:**
- **AI Study Planner**: Generates balanced weekly study plans considering task priorities, deadlines, and workload distribution
- **Daily Recommendations**: AI-powered task prioritization for optimal daily productivity
- **Quiz Generator**: Creates practice questions (multiple choice, true/false, short answer) from your notes to test understanding
- **Knowledge Assistant**: RAG-powered Q&A system that answers questions about your notes and tasks with conversation memory
- **Study Buddy Chat Mode**: 🆕 Interactive conversational AI tutor that maintains context throughout your study session (see details below)

**Content Enhancement:**
- **Note Expander**: AI-assisted content improvement with multiple modes:
  - `expand`: Add more detail and explanation
  - `clarify`: Improve clarity and explanation
  - `examples`: Add practical examples
  - `simplify`: Make content easier to understand

#### 💾 Data Storage
- **JSON-based Storage**: Simple, portable data storage in local JSON files
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Local First**: All data stored locally in the `data/` directory
- **No Database Required**: Lightweight storage with no external dependencies

### 🚀 Available Commands

Once StudyPal is running, you can use these commands:

#### Note Commands
```bash
add note "Title" [--tags tag1,tag2] [--content "content"]
    Create a new note with optional tags and content

list notes [--tag tagname]
    List all notes or filter by a specific tag

show note <id>
    Display a specific note with full details including linked notes

search notes "keyword"
    Search for notes (uses AI semantic search + keyword fallback)

update note <id> [--title "New Title"] [--content "content"] [--tags tag1,tag2]
    Update an existing note's title, content, or tags

delete note <id>
    Delete a note permanently

link note <id1> to <id2> [--type related]
    Create a connection between two notes (default type: related)
```

#### Task Commands
```bash
add task "Title" [--due YYYY-MM-DD] [--priority 1-5] [--desc "description"]
    Create a new task with optional due date, priority, and description

list tasks [--status todo|in_progress|done] [--priority 1-5]
    List all tasks or filter by status and/or priority

show task <id>
    Display a specific task with full details

update task <id> [--title "New Title"] [--status done] [--priority 4] [--due YYYY-MM-DD]
    Update an existing task's properties

delete task <id>
    Delete a task permanently

stats
    Show task statistics including completion rate, overdue, and upcoming tasks
```

#### AI Agent Commands (Requires OpenAI API Key)
```bash
suggest links <note_id>
    Get AI-powered suggestions for semantically related notes

suggest tags <note_id>
    Get AI-generated contextually relevant tag suggestions

plan week
    Generate an intelligent weekly study plan based on your tasks and priorities

plan today
    Get AI-recommended tasks to work on today based on priorities and deadlines

summary <note_id>
    Generate an AI-powered abstractive summary of a note

quiz <note_id> [--num 5]
    Generate quiz questions from a note (default: 5 questions)
    Supports multiple choice, true/false, and short answer formats

expand <note_id> [--mode expand|clarify|examples|simplify]
    AI-assisted note improvement (default mode: expand)

ask "your question"
    Ask questions about your notes and tasks - the AI remembers the conversation

clear conversation
    Clear the AI conversation history and start fresh

chat
    🆕 Enter interactive Study Buddy chat mode for conversational learning
    - Maintains context throughout your session
    - Quiz you on topics from your notes
    - Explain difficult concepts with examples
    - Provide personalized study strategies
    - Interactive Q&A with memory
    - Type 'bye', 'exit', or 'quit' to leave chat mode
```

#### General Commands
```bash
help
    Display help information about available commands

exit or quit
    Close StudyPal and save all data
```

### 🎓 Study Buddy Chat Mode

The **Study Buddy Chat Mode** is an interactive conversational AI tutor that provides a personalized learning experience:

**Key Features:**
- **Conversational Context**: Remembers your entire conversation within the session
- **Interactive Quizzing**: Request quizzes on any topic and get immediate feedback
- **Concept Explanations**: Get clear, simple explanations of difficult topics
- **Study Strategies**: Receive personalized advice on how to study effectively
- **Motivation & Support**: Encouraging feedback to keep you motivated

**Example Chat Session:**
```
studypal> chat

🎓 Study Buddy Chat Mode
Welcome! I'm your AI study buddy...

💭 You: Can you explain recursion?

🤖 Study Buddy: Recursion is when a function calls itself to solve 
a problem by breaking it down into smaller sub-problems...

💭 You: Show me an example

🤖 Study Buddy: [Provides example from your notes with explanation]

💭 You: Quiz me on this

🤖 Study Buddy: Great! Here's a question: [Creates quiz question]

💭 You: bye

👋 Thanks for studying with me!
Session summary: 3 message exchanges
```

See [CHAT_MODE.md](FinalProject/docs/CHAT_MODE.md) for complete details.

### 📦 Installation & Setup

**Prerequisites:**
- Python 3.11 or higher
- OpenAI API key (for AI features)

**Quick Start:**

1. Navigate to the FinalProject directory:
   ```powershell
   cd FinalProject
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```
   See [OPENAI_SETUP.md](FinalProject/docs/OPENAI_SETUP.md) for detailed setup instructions.

4. Run StudyPal:
   ```powershell
   py -m src.studypal
   ```

### 📚 Documentation

- **[FinalProject/README.md](FinalProject/README.md)**: Complete project documentation, usage guide, and technical details
- **[FinalProject/docs/OPENAI_SETUP.md](FinalProject/docs/OPENAI_SETUP.md)**: OpenAI API key configuration guide
- **[FinalProject/docs/CHAT_MODE.md](FinalProject/docs/CHAT_MODE.md)**: Study Buddy chat mode documentation
- **[FinalProject/docs/QUICKSTART.md](FinalProject/docs/QUICKSTART.md)**: Quick start guide for new users

### 🧪 Testing

The project includes comprehensive test coverage:

```powershell
# Run all tests
py -m pytest

# Run with verbose output
py -m pytest -v

# Run specific test file
py -m pytest tests/test_pkms.py

# Run with coverage
py -m pytest --cov=src.studypal
```

### 🏗️ Project Structure

```
FinalProject/
├── src/studypal/          # Main application code
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Entry point for module execution
│   ├── cli.py             # Command-line interface and command routing
│   ├── pkms.py            # Personal Knowledge Management System
│   ├── tasks.py           # Task management system
│   ├── agents.py          # AI agents (11 intelligent agents)
│   ├── storage.py         # JSON storage layer
│   └── utils.py           # Helper utilities
├── tests/                 # Comprehensive test suite
│   ├── test_pkms.py       # PKMS feature tests
│   ├── test_tasks.py      # Task management tests
│   ├── test_agents.py     # AI agent tests
│   └── test_openai.py     # OpenAI integration tests
├── data/                  # Local data storage
│   ├── notes.json         # Notes storage
│   └── tasks.json         # Tasks storage
├── docs/                  # Documentation
│   ├── OPENAI_SETUP.md    # API key setup guide
│   ├── CHAT_MODE.md       # Chat mode documentation
│   └── QUICKSTART.md      # Quick start guide
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

### 🔧 Technical Highlights

- **Modular Architecture**: Clean separation between PKMS, tasks, agents, and storage
- **AI Integration**: Seamless OpenAI API integration with 11 specialized AI agents
- **Cross-Platform**: Works on Windows, macOS, and Linux using pathlib
- **Extensible Design**: Easy to add new features and AI agents
- **Test Coverage**: Comprehensive pytest test suite
- **Type Hints**: Full type annotations for better code quality
- **Error Handling**: Graceful error handling and user-friendly messages

### 🎯 Use Cases

- **Study Organization**: Keep all your study notes organized with tags and links
- **Exam Preparation**: Generate quizzes and study plans for upcoming exams
- **Concept Learning**: Use chat mode to understand difficult concepts
- **Task Tracking**: Manage study tasks, assignments, and deadlines
- **Knowledge Building**: Build a connected knowledge graph of related topics
- **Time Management**: Get AI-powered daily and weekly study schedules

---

## 📂 Other Directories

- **tasks1/**: Basic task management system (JSON storage)
- **tasks2/**: Added PKMS with note management and tagging
- **tasks3/**: Restructured with proper package structure and testing
- **tasks4/**: Initial AI agent implementations
- **tasks5/**: Additional task management features
- **AI Chats/**: Development conversation logs and planning documents

---

## 📝 Development Notes

This project was developed iteratively, with each task building upon the previous one:

1. **tasks1**: Basic task manager with JSON storage
2. **tasks2**: Added Personal Knowledge Management System (PKMS)
3. **tasks3**: Restructured with proper Python packaging and pytest
4. **tasks4**: Integrated OpenAI and implemented AI agents
5. **FinalProject**: Combined all features with comprehensive AI capabilities

The development process is documented in the `AI Chats/` directory, showing the evolution of the project through various iterations.

---

## 📄 License

Educational project - CSC299 Final Project

## 👤 Author

Created as part of CSC299 coursework
