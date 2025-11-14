"""Simple test script to demonstrate the chat feature."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from studypal.storage import Storage
from studypal.pkms import PKMS
from studypal.tasks import TaskManager
from studypal.agents import StudyBuddyChat

# Initialize components
storage = Storage("data")
pkms = PKMS(storage)
task_manager = TaskManager(storage)

# Create some sample data if needed
notes = pkms.list_notes()
if len(notes) < 2:
    print("Adding sample notes for testing...")
    pkms.add_note("Python Basics", ["python", "programming"], 
                  "Python is a high-level programming language. Key concepts: variables, functions, loops.")
    pkms.add_note("Data Structures", ["python", "algorithms"],
                  "Common data structures: lists, dictionaries, sets, tuples. Each has different use cases.")

tasks = task_manager.list_tasks()
if len(tasks) < 2:
    print("Adding sample tasks for testing...")
    task_manager.add_task("Study Python loops", priority=3, description="Review for and while loops")
    task_manager.add_task("Practice algorithms", priority=4, description="Complete practice problems")

print("\n" + "="*70)
print("Chat Mode Demo")
print("="*70)
print("\nThis demonstrates the Study Buddy Chat feature.")
print("The chat mode provides an interactive AI tutor that:")
print("  • Has access to your notes and tasks")
print("  • Can quiz you on topics")
print("  • Explains concepts")
print("  • Provides study guidance")
print("\nTo use: Launch 'python -m studypal' and type 'chat'")
print("="*70 + "\n")

print("Would you like to see a quick demo? (y/n): ", end='')
choice = input().strip().lower()

if choice == 'y':
    print("\nLaunching Study Buddy Chat...")
    study_buddy = StudyBuddyChat(pkms, task_manager)
    
    # Start chat session
    try:
        study_buddy.start_chat_session()
    except KeyboardInterrupt:
        print("\n\nDemo ended.")
else:
    print("\nRun 'python -m studypal' and type 'chat' to try it yourself!")
