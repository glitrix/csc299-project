# Quick Start Guide - PKMS (Tasks2)

## Installation & Setup

1. **Navigate to the tasks2 directory:**
   ```bash
   cd c:\Users\joshk\CSC299\csc299-project\tasks2
   ```

2. **Test the installation:**
   ```bash
   py pkms.py --help
   ```

3. **Initialize with first command:**
   ```bash
   py pkms.py stats
   ```

## Essential Commands

### Quick Task Management
```bash
# Add a task
py pkms.py task add "Complete assignment" --priority high --due 2025-11-10

# List tasks
py pkms.py task list

# Mark task as in progress
py pkms.py task update 1 in_progress

# Complete a task
py pkms.py task complete 1
```

### Quick Note Taking
```bash
# Add a note
py pkms.py note add "Meeting Notes" --content "Key decisions made today"

# List notes
py pkms.py note list

# View full note
py pkms.py note view 1
```

### Quick Search
```bash
# Search everything
py pkms.py search "keyword"

# Search just tasks
py pkms.py search "keyword" --type tasks
```

### Quick Stats & Export
```bash
# View statistics
py pkms.py stats

# Export data
py pkms.py export --format markdown
```

## Run the Demo

To see all features in action:
```bash
py demo.py
```

## File Structure Created

After first use, you'll have:
```
tasks2/
├── pkms.py          # Main application
├── demo.py          # Interactive demonstration
├── README.md        # Full documentation
├── QUICKSTART.md    # This file
└── data/            # Auto-created data directory
    ├── tasks.json   # Your tasks
    ├── notes.json   # Your notes
    └── config.json  # System configuration
```

## Daily Workflow Example

```bash
# Morning: Check what's pending
py pkms.py task list --status pending

# Add today's tasks
py pkms.py task add "Review code" --priority high --due 2025-11-02

# Take notes during work
py pkms.py note add "Code Review Notes" --content "Found issue in auth module"

# Evening: Update progress
py pkms.py task update 1 completed
py pkms.py stats
```

## Help & Documentation

- `py pkms.py --help` - Main help
- `py pkms.py task --help` - Task commands
- `py pkms.py note --help` - Note commands
- See `README.md` for comprehensive documentation

## Differences from Tasks1

Tasks2 (PKMS) includes:
- ✅ Priority levels and due dates
- ✅ Note management system
- ✅ Advanced search capabilities
- ✅ Categories and tagging
- ✅ Export functionality
- ✅ Visual indicators and statistics
- ✅ Better CLI interface with argparse