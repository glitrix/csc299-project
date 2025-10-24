"""
Migration Script: Convert tasks.json to Markdown files

This script reads existing tasks from tasks.json and converts them
to individual Markdown files in the vault directory.
"""

import os
import json
from pathlib import Path
import storage_markdown

# Path to the JSON file
JSON_PATH = Path(__file__).parent / "tasks.json"


def migrate():
    """Migrate tasks from JSON to Markdown format."""
    if not JSON_PATH.exists():
        print("No tasks.json found. Nothing to migrate.")
        return
    
    print("Starting migration from JSON to Markdown...")
    print(f"Reading from: {JSON_PATH}")
    print(f"Writing to: {storage_markdown.VAULT_DIR}")
    print()
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Error: Could not read tasks.json. File may be corrupted.")
        return
    
    if not tasks:
        print("No tasks to migrate.")
        return
    
    print(f"Found {len(tasks)} tasks to migrate...")
    print()
    
    for task in tasks:
        title = task.get("title", "Untitled")
        desc = task.get("description", "")
        tid = task.get("id", None)
        completed = task.get("completed", False)
        created_at = task.get("created_at", None)
        
        # Save task as Markdown file
        saved_id, path = storage_markdown.save_task(
            title=title,
            description=desc,
            task_id=tid,
            completed=completed,
            created_at=created_at
        )
        
        status = "✓" if completed else "○"
        filename = os.path.basename(path)
        print(f"[{status}] Migrated Task {saved_id}: {title}")
        print(f"    → {filename}")
    
    print()
    print(f"✓ Migration complete! {len(tasks)} tasks converted to Markdown.")
    print(f"\nYour tasks are now stored in: {storage_markdown.VAULT_DIR}")
    print("\nYou can:")
    print("  1. Open the vault folder in Obsidian")
    print("  2. View/edit the Markdown files directly")
    print("  3. Continue using tasks.py (it will now use Markdown storage)")
    print()
    print("Note: Your original tasks.json is preserved as a backup.")


if __name__ == "__main__":
    migrate()
