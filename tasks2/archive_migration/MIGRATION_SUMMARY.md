# Migration to Markdown-Based PKM Storage

## Summary

Your task manager has been successfully migrated from JSON storage to a **Markdown-based Personal Knowledge Management (PKM) system**!

## What Changed

### Before
- Tasks stored in a single `tasks.json` file
- Required JSON parsing and writing

### After
- Each task is stored as an individual Markdown file in the `vault/` directory
- Files use **YAML frontmatter** (Obsidian-compatible format)
- Files are named with pattern: `{id}-{slug}.md`
- Human-readable and editable in any text editor

## File Structure

```
tasks1/
├── tasks.py                  # Main CLI (now uses Markdown storage)
├── storage_markdown.py       # Markdown storage backend
├── migrate_json_to_md.py     # Migration script (one-time use)
├── tasks.json                # Original backup (preserved)
└── vault/                    # New Markdown storage directory
    ├── 1-buy-groceries.md
    ├── 2-go-to-the-gym.md
    └── 3-test-pkm-storage.md
```

## Markdown File Format

Each task is stored with YAML frontmatter:

```markdown
---
id: 1
title: "Buy groceries"
description: "Milk, Bread, Eggs"
completed: true
created_at: "2025-10-15 11:05:32"
---

# Buy groceries

Milk, Bread, Eggs
```

## Benefits

1. **Obsidian Compatible**: Open the `vault/` folder in Obsidian to view and edit tasks
2. **Git-Friendly**: Each task is a separate file, better for version control
3. **Human-Readable**: No need for special tools to view/edit tasks
4. **Extensible**: Easy to add tags, links, and other Markdown features
5. **No External Dependencies**: Uses only Python standard library

## Usage

The CLI commands remain the same:

```bash
# Add a task
py tasks.py add "Task title" "Optional description"

# List all tasks
py tasks.py list

# Search tasks
py tasks.py search "keyword"

# Mark task as complete
py tasks.py complete <task_id>

# Show help
py tasks.py help
```

## Open in Obsidian

To use your tasks in Obsidian:

1. Open Obsidian
2. Click "Open folder as vault"
3. Select: `C:\Users\joshk\CSC299\csc299-project\tasks1\vault`
4. Your tasks will appear as individual notes!

## Next Steps (Optional Enhancements)

- Add tags support: `tags: [work, urgent]` in frontmatter
- Add due dates: `due_date: "2025-10-30"` in frontmatter
- Link tasks together using Obsidian's `[[Task Name]]` syntax
- Add categories/folders within the vault
- Sync with Obsidian Sync or Git for backup

## Testing Results

✅ Migration successful (2 tasks converted)
✅ List command working
✅ Add command working (created task #3)
✅ Search command working
✅ Complete command working (marked task #2 as complete)

## Backup

Your original `tasks.json` file is preserved as a backup in case you need to revert.
