# STUDYPAL_SPEC.md

A precise, implementation-ready spec for **StudyPal** — a terminal-first study assistant that combines a **Personal Knowledge Management System (PKMS)**, **task management**, a **terminal chat interface**, and **local AI-style agents** to suggest links, flashcards, and study plans.

> **Hard constraint:** This project is **strictly Python-only**. No non-Python runtimes or services. It must run on Windows, macOS, and Linux.

---

## 1) Goals & Scope

- Capture and organize study notes (Markdown) with tags and backlinks.
- Manage tasks (assignments, readings, milestones) with due dates and priorities.
- Provide a **chat-style terminal interface** for commands and results.
- Include **local agents** that:
  - suggest backlinks and tags for new notes,
  - extract flashcards from notes,
  - generate a 7-day study plan from tasks and constraints.
- Persist state locally (default: **SQLite**). JSON files allowed for prototyping.
- Be testable, deterministic, offline-first. Any LLM usage must be optional and disabled by default.

**Non-goals:** web UI; cloud sync; multi-user; external APIs by default.

---

## 2) Hard Requirements & Constraints

- **Language:** Python 3.11+ **only**.
- **OS:** Windows, macOS, Linux; no OS-specific features. Use `pathlib` and `tempfile`.
- **State:** SQLite (primary). JSON allowed in `/prototypes` only. No networked DB.
- **Offline-first:** All core features work without internet or API keys.
- **Determinism:** Agents ship **heuristic** implementations with deterministic outputs for tests.
- **Optional LLM backend:** If enabled via env var (`STUDYPAL_LLM=1`), it **must not** be required for tests or core flows.
- **Dependencies:** Keep minimal; pin exact versions in `requirements.txt`. Avoid platform-problematic libs.
- **License:** MIT (default).
- **CLI UX:** Single entrypoint `studypal` (via `console_scripts`) opens a chat loop.
- **Tests:** `pytest` with >80% coverage on core modules. No network during tests.

---

## 3) Repository Structure

```
/studypal
  ├─ src/studypal/
  │   ├─ app.py                 # main chat loop (REPL)
  │   ├─ ui/chat.py             # parser, command routing, rendering
  │   ├─ config.py              # config & env handling
  │   ├─ db.py                  # sqlite connection + migrations
  │   ├─ common/types.py        # dataclasses / TypedDicts / Enums
  │   ├─ pkms/
  │   │   ├─ models.py          # Note, Tag, Link, Card
  │   │   ├─ storage.py         # repo interfaces & sqlite impl
  │   │   ├─ search.py          # FTS5 search helpers
  │   │   └─ cards.py           # spaced repetition scheduler (SM-2)
  │   ├─ tasks/
  │   │   ├─ models.py          # Task, Project
  │   │   ├─ storage.py         # repo interfaces & sqlite impl
  │   │   └─ planner.py         # 7-day plan heuristics
  │   ├─ agents/
  │   │   ├─ linker.py          # backlink/tag suggester (TF-IDF)
  │   │   ├─ cardsmith.py       # flashcard extractor from notes
  │   │   ├─ planbot.py         # calls tasks.planner
  │   │   └─ llm.py             # optional LLM hooks (disabled by default)
  │   └─ utils/
  │       ├─ text.py            # tokenization, ngrams, normalization
  │       └─ tables.py          # ASCII/markdown table rendering
  ├─ tests/
  │   ├─ test_notes.py
  │   ├─ test_tasks.py
  │   ├─ test_cards.py
  │   ├─ test_agents.py
  │   └─ test_cli.py
  ├─ prototypes/                # discarded JSON-first explorations
  ├─ README.md
  ├─ SUMMARY.md
  ├─ video.txt
  ├─ requirements.txt
  ├─ pyproject.toml             # build + console_scripts
  └─ LICENSE
```

---

## 4) Data Model (SQLite, FTS5)

Use `sqlite3` with PRAGMAs for reliability. Enable FTS5 for note search.

```sql
-- Notes & Linking
CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  body_md TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
  title, body_md, content='notes', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
  INSERT INTO notes_fts(rowid, title, body_md) VALUES (new.id, new.title, new.body_md);
END;
CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
  UPDATE notes_fts SET title=new.title, body_md=new.body_md WHERE rowid=new.id;
END;
CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
  DELETE FROM notes_fts WHERE rowid=old.id;
END;

CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS note_tags (
  note_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY (note_id, tag_id),
  FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS links (
  src_id INTEGER NOT NULL,
  dst_id INTEGER NOT NULL,
  rel TEXT NOT NULL DEFAULT 'related',
  PRIMARY KEY (src_id, dst_id, rel),
  FOREIGN KEY (src_id) REFERENCES notes(id) ON DELETE CASCADE,
  FOREIGN KEY (dst_id) REFERENCES notes(id) ON DELETE CASCADE
);

-- Tasks
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT DEFAULT '',
  status TEXT NOT NULL DEFAULT 'todo', -- todo|doing|done|blocked
  priority INTEGER NOT NULL DEFAULT 2, -- 1..5 (5 highest)
  due_at TEXT,                         -- ISO8601
  project TEXT DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Flashcards (SM-2 scheduling)
CREATE TABLE IF NOT EXISTS cards (
  id INTEGER PRIMARY KEY,
  note_id INTEGER NOT NULL,
  prompt TEXT NOT NULL,
  answer TEXT NOT NULL,
  ease REAL NOT NULL DEFAULT 2.5,
  interval INTEGER NOT NULL DEFAULT 0,   -- days
  reps INTEGER NOT NULL DEFAULT 0,
  lapses INTEGER NOT NULL DEFAULT 0,
  due_at TEXT NOT NULL,                  -- ISO8601
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);
```

**Time format:** ISO8601 UTC strings (e.g., `2025-11-12T15:04:05Z`).

---

## 5) Core Domain Types (Python)

```python
# src/studypal/common/types.py
from dataclasses import dataclass
from typing import Literal, Optional, Sequence

Status = Literal["todo", "doing", "done", "blocked"]

@dataclass
class Note:
    id: int | None
    title: str
    body_md: str
    tags: Sequence[str] = ()
    created_at: str | None = None
    updated_at: str | None = None

@dataclass
class Task:
    id: int | None
    title: str
    body: str = ""
    status: Status = "todo"
    priority: int = 2
    due_at: Optional[str] = None
    project: str = ""
    created_at: str | None = None
    updated_at: str | None = None

@dataclass
class Card:
    id: int | None
    note_id: int
    prompt: str
    answer: str
    ease: float = 2.5
    interval: int = 0
    reps: int = 0
    lapses: int = 0
    due_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
```
---

## 6) Terminal Chat Interface (REPL)

- **Entry:** `studypal` opens a prompt like `studypal>`.
- **Format:** Each line is a command; results printed below. Support quotes and flags.
- **Errors:** Human-readable message + non-zero exit code only for unrecoverable CLI issues.

### Command Grammar (initial)

| Command | Example | Behavior |
|---|---|---|
| `add note "<title>" [--tags t1,t2]` | `add note "Backprop" --tags ml,study` | Create note. Opens ID in output. |
| `open note <id>` | `open note 12` | Show title, tags, body. |
| `edit note <id> --title "New" --body "..." --tags +a,-b` |  | Update fields; `+` add, `-` remove tags. |
| `find notes "<query>"` | `find notes "chain rule"` | FTS search title/body. |
| `link <src> -> <dst> [rel]` | `link 12 -> 7 related` | Create backlink. |
| `add task "<title>" [--due YYYY-MM-DD] [--prio 1..5] [--project P]` | `add task "Finish PS5" --due 2025-11-20 --prio 4 --project Math` | Create task. |
| `next [--limit N]` | `next --limit 5` | Show prioritized list by overdue/due/priority. |
| `task <id> set status <todo|doing|done|blocked>` | `task 14 set status doing` | Update status. |
| `review` | `review` | Start flashcard session due today. |
| `card add <note_id> "<prompt>" "<answer>"` | `card add 12 "What is ..." "It is ..."` | Manual card. |
| `agent link-suggest <note_id>` | `agent link-suggest 12` | Suggest backlinks/tags. |
| `agent cardsmith <note_id>` | `agent cardsmith 12` | Propose flashcards from note. |
| `agent plan-week [--capacity H]` | `agent plan-week --capacity 2.5` | 7-day plan based on tasks. |
| `export week --format md` |  | Emit Markdown schedule for next 7 days. |
| `help` / `?` |  | List commands. |
| `quit` / `exit` |  | End session. |

**Natural language aliases (limited, deterministic):**  
Implement simple intent patterns for: “add a task to X by {date}”, “find notes about Y”, “what should I do next?”. Avoid full NLP; use regex-based slots.

---

## 7) Agents (Deterministic Heuristics)

### 7.1 Linker (`agents/linker.py`)
- **Input:** note_id
- **Process:**  
  - Normalize tokens (lowercase, strip punctuation).  
  - Compute TF-IDF for the new note vs existing notes (`sklearn` optional; otherwise a tiny local TF-IDF).  
  - Cosine similarity → top-k (default 5) above threshold (e.g., 0.22).  
  - Tag suggestions: top frequent tags from similar notes.
- **Output:** suggestions list `{dst_id, score, rel="related"}`, `{tag, score}`.
- **Side effects:** None by default; offer to create `tasks` like “Confirm link 12 ↔ 7”.

### 7.2 Cardsmith (`agents/cardsmith.py`)
- **Input:** note_id
- **Process:**  
  - Parse headings and bullet lines; extract Q/A pairs by rules:  
    - Inline flashcards `{{q: ... | a: ...}}`  
    - “Term — Definition” lines → card  
    - “Q: … A: …” blocks  
  - Deduplicate by prompt hash.  
- **Output:** `Card` candidates (not yet persisted unless user accepts).

### 7.3 PlanBot (`agents/planbot.py`)
- **Input:** tasks, capacity hours/day (default 2h)
- **Process:**  
  - Score `s = w1*overdue + w2*due_soon + w3*priority`, with `overdue∈{0,1}`, `due_soon = max(0, 1 - days_until_due/7)`. Suggested defaults: `w1=3, w2=2, w3=1`.  
  - Greedy pack tasks into the next 7 days without exceeding daily capacity.  
  - Split long tasks into sub-sessions of 30–90 minutes blocks.
- **Output:** plan for 7 days with assignments per day.

### 7.4 Optional LLM (`agents/llm.py`)
- Disabled by default. If `STUDYPAL_LLM=1` and `OPENAI_API_KEY` present, expose **advisory** alternatives that mirror the heuristic outputs. All unit tests must target heuristics.

---

## 8) Spaced Repetition (SM-2)

Implement standard SM-2 with quality score `q ∈ {0..5}` input by user during `review`.

Update rules:
```
if q < 3: interval = 1; lapses += 1
else:
  if reps == 0: interval = 1
  elif reps == 1: interval = 6
  else: interval = round(interval * ease)
ease = max(1.3, ease + (0.1 - (5 - q)*(0.08 + (5 - q)*0.02)))
reps = reps + 1 if q >= 3 else 0
due_at = today + interval days
```

UI prompts during review:
- Show prompt, wait for `[Enter]` to reveal answer, then ask `Score (0-5)?`.  
- Update card, show next due date.

---

## 9) Planning & Scheduling Logic

### Task prioritization for `next`
1. Overdue first (earliest due first),
2. Due within 7 days (earliest first),
3. Then by priority desc,
4. Then recently created.

### Weekly plan generation
- Capacity per day defaults to 2.0h; configurable.
- Break tasks into 30–90 min suggested blocks.
- Respect due dates: tasks with due date can’t be scheduled after due date.

---

## 10) Configuration

- File locations (default within user home):
  - Database: `~/.studypal/db.sqlite3`
  - Logs: `~/.studypal/logs/studypal.log`
- Env vars:
  - `STUDYPAL_HOME`: override base dir
  - `STUDYPAL_LLM`: `"1"` to enable optional LLM hooks (not used in tests)
  - `OPENAI_API_KEY`: used only if `STUDYPAL_LLM=1`
- CLI flags:
  - `--db PATH` (for tests and ephemeral runs)
  - `--no-color` (disable ANSI)
  - `--export PATH` (where exports go)

---

## 11) Logging & Errors

- Use `logging` (INFO default, DEBUG via `STUDYPAL_LOG=debug`).
- Log SQL migrations at INFO.
- Fail fast on schema mismatch; provide `studypal --migrate` command.

---

## 12) Testing Requirements (pytest)

- **Unit:** CRUD for notes, tags, links; FTS search; tasks sorting; SM-2 updates (table tests); agents with fixed fixtures.  
- **CLI:** simulate commands via Typer/CliRunner; assert stdout strings.  
- **No network**; force `STUDYPAL_LLM` off in tests.
- **Coverage:** ≥80% on `src/studypal` excluding `agents/llm.py`.

---

## 13) Migrations

- On startup, run `PRAGMA user_version`; apply forward SQL if needed.
- Store SQL migration files under `src/studypal/migrations/NNN.sql`.
- Never silently drop data; print prompt if destructive migration is attempted (require `--yes`).

---

## 14) Rendering Rules (Terminal)

- Use plain text with minimal ANSI (optional): headings, tables, code blocks.
- Prefer monospace tables for lists (notes, tasks, plan).
- Wrap lines at 100 chars for readability.

---

## 15) Security & Privacy

- All data is local. No telemetry.  
- If LLM optional mode is enabled, show a warning and require explicit confirmation once per session.  
- Redact secrets from logs.

---

## 16) Performance Targets

- 1k notes, 5k tasks: search < 150ms; `next` < 100ms; `agent link-suggest` < 1s on a mid-tier laptop.
- Cold start (create DB + migrations) < 1.5s.

---

## 17) Deliverables Mapping

- **Final software:** in `src/studypal`, executable `studypal`.
- **Commits:** granular with messages: `spec:`, `feat:`, `fix:`, `test:`, `docs:`.
- **Prototypes:** `/prototypes` JSON-first experiments committed then discarded.
- **`video.txt`**: contains a single YouTube URL (6–8 min demo).
- **`SUMMARY.md`**: explains planning, AI-assistant modes, what worked/failed (detailed; >500 words recommended).

---

## 18) Acceptance Criteria (must pass)

1. `studypal` starts a REPL and accepts at least the commands listed in §6.  
2. Notes can be created, tagged, linked, searched (FTS5) and opened.  
3. Tasks can be created, listed via `next`, updated (status/priority/due), and exported weekly.  
4. `review` session uses SM-2 and persists updates.  
5. Agents run locally with deterministic heuristics and produce non-empty, sensible suggestions on realistic fixtures.  
6. Works on Windows/macOS/Linux (tested via CI matrix or manual verification instructions).  
7. All core functions pass tests with LLM disabled.  
8. No internet required for tests or core usage.  
9. **Python-only** codebase and dependencies.

---

## 19) Implementation Notes & Patterns

- Use repository pattern for storage (`storage.py`), exposing pure functions suitable for unit tests.  
- Keep `datetime` in UTC; centralize now() in a single function to make tests stable (allow freeze).  
- Write small utilities for tokenization and similarity; keep them deterministic (fixed stopword list, fixed stemming rules or none).  
- Guard LLM code paths with `if settings.llm_enabled:` and keep outputs advisory (never required).

---

## 20) Stretch (Optional, not graded-critical)

- Export `.ics` for the weekly plan.  
- ASCII charts for review counts and streaks.  
- `import` from a folder of Markdown notes (frontmatter tags).  
- `project` concept for tasks + notes linkage.

---

## 21) Example Session (Happy Path)

```
$ studypal
studypal> add note "Backprop" --tags ml,study
[✓] Note 12 created.

studypal> find notes "chain rule"
#12 Backprop — tags: ml,study
  ... shows snippet ...

studypal> agent link-suggest 12
Suggestions:
  link to #7 "Gradients 101" (score 0.31)
  tags: calculus (0.44)

studypal> add task "Finish PS5" --due 2025-11-20 --prio 4 --project Math
[✓] Task 14 created.

studypal> next --limit 3
1) [prio 4] Finish PS5 (due 2025-11-20)  id:14
...

studypal> review
Card 1/10 — Press Enter to reveal.
Q: What is the chain rule?
A: ...
Score (0-5)? 4
[✓] Next due in 6 days.

studypal> agent plan-week --capacity 2.5
Mon: Finish PS5 (60m), Read Backprop note (30m) ...
...

studypal> export week --format md
[✓] ./week-plan.md
```

---

## 22) Dependencies (pin exact versions)

- `rich==13.9.2` (optional ANSI tables; can be toggled off)
- `typer==0.12.4` (CLI ergonomics) or `cmd2==2.4.3` (choose one)
- `pytest==8.3.3`
- `python-dateutil==2.9.0.post0`
- *(Optional)* `scikit-learn==1.5.2` for TF-IDF; if omitted, implement tiny TF-IDF locally.

> All dependencies must be pure-Python or ship wheels for Win/macOS/Linux. No C compiler requirement for base install.

---

## 23) Out of Scope

- Web server, GUI, cloud sync, authentication, multi-user, calendar APIs, browser automation.

---

## 24) Build & Run

- Install: `pip install -e .`  
- Run: `studypal`  
- Test: `pytest -q`  
- LLM optional: `STUDYPAL_LLM=1 OPENAI_API_KEY=... studypal` (not used in tests; must be fully optional)

---

**This spec is intentionally explicit to feed into an AI coding assistant. Honor all “strictly Python-only” requirements, keep the heuristic agents deterministic, and ensure the terminal experience is fast and pleasant.**
