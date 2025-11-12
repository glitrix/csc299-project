"""Quick verification script to test StudyPal functionality."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.studypal.storage import Storage
from src.studypal.pkms import PKMS
from src.studypal.tasks import TaskManager
from src.studypal.agents import LinkSuggester, StudyPlanner

print("=" * 70)
print("StudyPal Quick Verification Test")
print("=" * 70)

# Create temporary storage
import tempfile
temp_dir = tempfile.mkdtemp()
print(f"\nUsing temporary directory: {temp_dir}")

# Initialize components
storage = Storage(temp_dir)
pkms = PKMS(storage)
task_manager = TaskManager(storage)

print("\n1. Testing PKMS...")
note1_id = pkms.add_note("Python Basics", "Learn Python programming", ["python", "programming"])
note2_id = pkms.add_note("Python Advanced", "Advanced Python concepts", ["python", "advanced"])
print(f"   ✓ Created notes #{note1_id} and #{note2_id}")

notes = pkms.list_notes()
print(f"   ✓ Listed {len(notes)} notes")

search_results = pkms.search_notes("python")
print(f"   ✓ Found {len(search_results)} notes matching 'python'")

pkms.link_notes(note1_id, note2_id)
print(f"   ✓ Linked notes #{note1_id} and #{note2_id}")

print("\n2. Testing Task Management...")
task_id = task_manager.add_task("Study Python", "Complete chapter 1", priority=4, due_date="2025-11-20")
print(f"   ✓ Created task #{task_id}")

tasks = task_manager.list_tasks()
print(f"   ✓ Listed {len(tasks)} tasks")

task_manager.mark_in_progress(task_id)
print(f"   ✓ Marked task #{task_id} as in progress")

stats = task_manager.get_statistics()
print(f"   ✓ Statistics: {stats['total']} total, {stats['in_progress']} in progress")

print("\n3. Testing AI Agents...")
link_suggester = LinkSuggester(pkms)
suggestions = link_suggester.suggest_links(note1_id)
print(f"   ✓ Link suggester found {len(suggestions)} suggestions")

study_planner = StudyPlanner(task_manager, pkms)
plan = study_planner.plan_week()
print(f"   ✓ Generated weekly plan with {len(plan)} days")

daily = study_planner.suggest_daily_schedule()
print(f"   ✓ Daily schedule has {len(daily)} recommended tasks")

print("\n" + "=" * 70)
print("✓ All tests passed successfully!")
print("=" * 70)
print("\nTo run StudyPal interactively, use:")
print("  python -m src.studypal")
print("\nFor help, type 'help' when running StudyPal")
print("=" * 70)

# Cleanup
import shutil
shutil.rmtree(temp_dir)
