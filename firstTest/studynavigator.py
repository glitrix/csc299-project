#!/usr/bin/env python3
"""
StudyNavigator — Minimal Prototype (Single File)

Features
- JSON storage (portable) in ~/.studynav/{notes.json,tasks.json}
- Typer-based CLI with Rich output
- Notes: add, list, show, edit (append), tag
- Tasks: add, list (filters), done, link to a note
- Search: substring over titles/bodies

Quickstart
  python -m venv .venv
  # Windows: .venv\Scripts\activate
  # macOS/Linux: source .venv/bin/activate
  python -m pip install -U pip
  pip install -r requirements.txt

  python studynavigator.py --help
  python studynavigator.py note add "Lecture 1: DP" --body "Overlapping subproblems" --tags algorithms cs101
  python studynavigator.py task add "Write DP cheatsheet" --prio 2 --due 2025-10-20 --note <NOTE_ID>
  python studynavigator.py search "DP"

Notes
- This is a starter prototype; swap JSON for SQLite + FTS later.
- IDs are time-based for readability; not guaranteed globally unique, but low collision.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
import uuid

import typer
from rich.console import Console
from rich.table import Table
from rich import box

APP_NAME = "studynav"
DATA_DIR = Path(os.path.expanduser("~")) / f".{APP_NAME}"
NOTES_PATH = DATA_DIR / "notes.json"
TASKS_PATH = DATA_DIR / "tasks.json"

console = Console()
app = typer.Typer(no_args_is_help=True, add_completion=False)
note_app = typer.Typer(no_args_is_help=True)
task_app = typer.Typer(no_args_is_help=True)
app.add_typer(note_app, name="note", help="Work with notes")
app.add_typer(task_app, name="task", help="Work with tasks")

# -----------------------------
# Models
# -----------------------------

def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def new_id(prefix: str) -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    short = uuid.uuid4().hex[:6]
    return f"{prefix}_{ts}_{short}"

@dataclass
class Note:
    id: str
    title: str
    body: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

@dataclass
class Task:
    id: str
    title: str
    status: str = "todo"  # todo|doing|done
    priority: int = 3      # 1 (high) .. 5 (low)
    due_date: Optional[str] = None  # YYYY-MM-DD
    note_id: Optional[str] = None
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

# -----------------------------
# Storage (JSON)
# -----------------------------
class JsonStore:
    def __init__(self, file_path: Path, kind: str):
        self.file_path = file_path
        self.kind = kind
        self._ensure_file()

    def _ensure_file(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"items": []}, f)

    def _load(self) -> Dict[str, Any]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]):
        tmp = self.file_path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(self.file_path)

    # Generic helpers
    def list_items(self) -> List[Dict[str, Any]]:
        return self._load()["items"]

    def get(self, item_id: str) -> Optional[Dict[str, Any]]:
        for it in self.list_items():
            if it.get("id") == item_id:
                return it
        return None

    def upsert(self, item: Dict[str, Any]):
        data = self._load()
        items = data["items"]
        for i, it in enumerate(items):
            if it.get("id") == item["id"]:
                items[i] = item
                self._save(data)
                return
        items.append(item)
        self._save(data)

    def replace_all(self, items: List[Dict[str, Any]]):
        self._save({"items": items})

notes_store = JsonStore(NOTES_PATH, "note")
tasks_store = JsonStore(TASKS_PATH, "task")

# -----------------------------
# Render helpers
# -----------------------------

def render_notes(notes: List[Note]):
    t = Table(title=f"Notes ({len(notes)})", box=box.SIMPLE_HEAVY)
    t.add_column("ID", style="cyan", no_wrap=True)
    t.add_column("Title", style="bold")
    t.add_column("Tags", style="magenta")
    t.add_column("Updated", style="dim")
    for n in notes:
        t.add_row(n.id, n.title, ", ".join(n.tags), n.updated_at)
    console.print(t)


def render_tasks(tasks: List[Task]):
    t = Table(title=f"Tasks ({len(tasks)})", box=box.SIMPLE_HEAVY)
    t.add_column("ID", style="cyan", no_wrap=True)
    t.add_column("Title", style="bold")
    t.add_column("Due", style="yellow")
    t.add_column("Prio", justify="right")
    t.add_column("Status")
    t.add_column("Note")
    for x in tasks:
        t.add_row(x.id, x.title, x.due_date or "-", str(x.priority), x.status, x.note_id or "-")
    console.print(t)

# -----------------------------
# Converters
# -----------------------------
def dict_to_note(d: Dict[str, Any]) -> Note:
    return Note(**d)

def dict_to_task(d: Dict[str, Any]) -> Task:
    return Task(**d)

# -----------------------------
# CLI: Notes
# -----------------------------
@note_app.command("add")
def note_add(
    title: str = typer.Argument(..., help="Note title"),
    body: str = typer.Option("", "--body", help="Note body text"),
    tags: List[str] = typer.Argument(None, help="Optional tags", show_default=False),
):
    """Create a new note."""
    n = Note(id=new_id("n"), title=title, body=body, tags=tags or [])
    notes_store.upsert(asdict(n))
    console.print(f"[green]Created note[/] {n.id} : [bold]{n.title}[/]")

@note_app.command("list")
def note_list(
    tag: Optional[str] = typer.Option(None, "--tag", help="Filter by tag"),
):
    """List notes (optionally by tag)."""
    items = [dict_to_note(x) for x in notes_store.list_items()]
    if tag:
        items = [n for n in items if tag in n.tags]
    items.sort(key=lambda n: n.updated_at, reverse=True)
    render_notes(items)

@note_app.command("show")
def note_show(note_id: str):
    """Show a note by ID."""
    d = notes_store.get(note_id)
    if not d:
        console.print(f"[red]Note not found:[/] {note_id}")
        raise typer.Exit(1)
    n = dict_to_note(d)
    console.rule(f"{n.title} ({n.id})")
    if n.tags:
        console.print(f"[magenta]tags:[/] {', '.join(n.tags)}\n")
    console.print(n.body)

@note_app.command("append")
def note_append(note_id: str, text: str = typer.Argument(..., help="Text to append")):
    d = notes_store.get(note_id)
    if not d:
        console.print(f"[red]Note not found:[/] {note_id}")
        raise typer.Exit(1)
    n = dict_to_note(d)
    n.body = (n.body + "\n\n" + text).strip()
    n.updated_at = now_iso()
    notes_store.upsert(asdict(n))
    console.print(f"[green]Updated note[/] {n.id}")

# -----------------------------
# CLI: Tasks
# -----------------------------
@task_app.command("add")
def task_add(
    title: str = typer.Argument(..., help="Task title"),
    prio: int = typer.Option(3, "--prio", min=1, max=5, help="Priority 1-5"),
    due: Optional[str] = typer.Option(None, "--due", help="YYYY-MM-DD"),
    note: Optional[str] = typer.Option(None, "--note", help="Link to a note id"),
):
    t = Task(id=new_id("t"), title=title, priority=prio, due_date=due, note_id=note)
    tasks_store.upsert(asdict(t))
    console.print(f"[green]Created task[/] {t.id} : [bold]{t.title}[/]")

@task_app.command("list")
def task_list(
    status: Optional[str] = typer.Option(None, "--status", help="todo|doing|done"),
    due_before: Optional[str] = typer.Option(None, "--due-before", help="YYYY-MM-DD"),
    note: Optional[str] = typer.Option(None, "--note", help="Filter by note id"),
):
    items = [dict_to_task(x) for x in tasks_store.list_items()]
    if status:
        items = [t for t in items if t.status == status]
    if note:
        items = [t for t in items if t.note_id == note]
    if due_before:
        items = [t for t in items if t.due_date and t.due_date <= due_before]
    # Sort: status(todo->doing->done), then due date asc, then prio asc
    order = {"todo": 0, "doing": 1, "done": 2}
    items.sort(key=lambda t: (order.get(t.status, 9), t.due_date or "9999-99-99", t.priority))
    render_tasks(items)

@task_app.command("done")
def task_done(task_id: str):
    d = tasks_store.get(task_id)
    if not d:
        console.print(f"[red]Task not found:[/] {task_id}")
        raise typer.Exit(1)
    t = dict_to_task(d)
    t.status = "done"
    t.updated_at = now_iso()
    tasks_store.upsert(asdict(t))
    console.print(f"[green]Completed task[/] {t.id}")

# -----------------------------
# CLI: Search (simple substring)
# -----------------------------
@app.command("search")
def search(query: str = typer.Argument(..., help="Search text")):
    query_lower = query.lower()
    notes = [dict_to_note(x) for x in notes_store.list_items()]
    tasks = [dict_to_task(x) for x in tasks_store.list_items()]

    matched_notes = [n for n in notes if query_lower in n.title.lower() or query_lower in n.body.lower()]
    matched_tasks = [t for t in tasks if query_lower in t.title.lower()]

    console.rule(f"Search results for: {query}")
    if matched_notes:
        render_notes(matched_notes)
    else:
        console.print("[dim]No notes matched.[/]")

    if matched_tasks:
        render_tasks(matched_tasks)
    else:
        console.print("[dim]No tasks matched.[/]")

# -----------------------------
# Utility: Init / Paths
# -----------------------------
@app.command("where")
def where():
    """Show storage paths."""
    console.print(f"Data dir: [cyan]{DATA_DIR}[/]")
    console.print(f"Notes:    [cyan]{NOTES_PATH}[/]")
    console.print(f"Tasks:    [cyan]{TASKS_PATH}[/]")

@app.callback()
def _main():
    """StudyNavigator minimal prototype. Use subcommands `note`, `task`, and `search`."""
    pass

if __name__ == "__main__":
    app()
