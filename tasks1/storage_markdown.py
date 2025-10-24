"""
Markdown Storage Backend for Task Manager

This module provides functions to store tasks as individual Markdown files
in an Obsidian-style vault with YAML frontmatter.
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Any

# Vault directory where Markdown files will be stored
VAULT_DIR = os.path.join(os.path.dirname(__file__), "vault")
os.makedirs(VAULT_DIR, exist_ok=True)


def _slugify(s: str) -> str:
    """Convert a string to a URL-friendly slug."""
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s or 'task'


def _next_id() -> int:
    """Find the next available task ID by scanning existing files."""
    max_id = 0
    for name in os.listdir(VAULT_DIR):
        m = re.match(r'^(\d+)-', name)
        if m:
            try:
                max_id = max(max_id, int(m.group(1)))
            except ValueError:
                pass
    return max_id + 1


def save_task(title: str, description: str = "", task_id: int = None, 
              completed: bool = False, created_at: str = None) -> tuple:
    """
    Save a task as a Markdown file with YAML frontmatter.
    
    Args:
        title: Task title
        description: Task description (optional)
        task_id: Task ID (auto-generated if not provided)
        completed: Completion status
        created_at: Creation timestamp (auto-generated if not provided)
    
    Returns:
        Tuple of (task_id, file_path)
    """
    tid = task_id if task_id else _next_id()
    slug = _slugify(title)
    filename = f"{tid}-{slug}.md"
    path = os.path.join(VAULT_DIR, filename)
    
    if created_at is None:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # YAML frontmatter (Obsidian-friendly)
    completed_str = "true" if completed else "false"
    front = [
        "---",
        f"id: {tid}",
        f"title: \"{title.replace('\"', '\\\"')}\"",
        f"description: \"{description.replace('\"', '\\\"')}\"",
        f"completed: {completed_str}",
        f"created_at: \"{created_at}\"",
        "---",
        "",
    ]
    
    # Markdown body
    body = [f"# {title}", ""]
    if description:
        body.extend([description, ""])
    
    content = "\n".join(front + body)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return tid, path


def list_tasks() -> List[Dict[str, Any]]:
    """
    List all tasks by reading Markdown files from the vault.
    
    Returns:
        List of task dictionaries
    """
    tasks = []
    for name in sorted(os.listdir(VAULT_DIR)):
        path = os.path.join(VAULT_DIR, name)
        if not os.path.isfile(path) or not name.endswith('.md'):
            continue
        
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        
        # Parse YAML frontmatter
        meta = {}
        if lines and lines[0].strip() == "---":
            i = 1
            while i < len(lines) and lines[i].strip() != "---":
                line = lines[i].strip()
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"')
                i += 1
        
        # Ensure minimal fields
        tasks.append({
            "id": int(meta.get("id", 0)),
            "title": meta.get("title", ""),
            "description": meta.get("description", ""),
            "completed": meta.get("completed", "false").lower() == "true",
            "created_at": meta.get("created_at", ""),
            "file": path
        })
    
    return tasks


def mark_complete(task_id: int) -> bool:
    """
    Mark a task as complete by updating its Markdown file.
    
    Args:
        task_id: ID of the task to mark complete
    
    Returns:
        True if successful, False if task not found
    """
    for name in os.listdir(VAULT_DIR):
        if name.startswith(f"{task_id}-"):
            path = os.path.join(VAULT_DIR, name)
            
            with open(path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            
            # Update the completed field in frontmatter
            out = []
            in_front = False
            for i, line in enumerate(lines):
                if i == 0 and line.strip() == "---":
                    in_front = True
                    out.append(line)
                    continue
                if in_front and line.strip().startswith("completed:"):
                    out.append("completed: true")
                    continue
                if in_front and line.strip() == "---":
                    in_front = False
                    out.append(line)
                    continue
                out.append(line)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(out))
            
            return True
    
    return False


def search_tasks(keyword: str) -> List[Dict[str, Any]]:
    """
    Search tasks by keyword in title or description.
    
    Args:
        keyword: Search keyword
    
    Returns:
        List of matching task dictionaries
    """
    all_tasks = list_tasks()
    keyword_lower = keyword.lower()
    
    return [
        task for task in all_tasks
        if keyword_lower in task['title'].lower() or 
           keyword_lower in task['description'].lower()
    ]


def delete_task(task_id: int) -> bool:
    """
    Delete a task by removing its Markdown file.
    
    Args:
        task_id: ID of the task to delete
    
    Returns:
        True if successful, False if task not found
    """
    for name in os.listdir(VAULT_DIR):
        if name.startswith(f"{task_id}-"):
            path = os.path.join(VAULT_DIR, name)
            try:
                os.remove(path)
                return True
            except OSError:
                return False
    
    return False
