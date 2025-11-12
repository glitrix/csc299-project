"""Test script to verify all AI-powered features work correctly."""

import os
import sys

# Check for API key first
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in environment.")
    print("Please set up your API key before running this test.")
    print("See OPENAI_SETUP.md for instructions.")
    sys.exit(1)

print("✓ OpenAI API key found")
print("\n" + "="*70)
print("Testing AI-Powered Features")
print("="*70 + "\n")

from src.studypal.storage import Storage
from src.studypal.pkms import PKMS
from src.studypal.tasks import TaskManager
from src.studypal.agents import (
    LinkSuggester, TagSuggester, StudyPlanner, SummaryGenerator,
    SemanticSearchAgent, QuizGenerator, KnowledgeAssistant, NoteExpander
)

# Initialize components
print("1. Initializing components...")
storage = Storage("test_data")
pkms = PKMS(storage)
task_manager = TaskManager(storage)

# Create test data
print("2. Creating test notes...")
note1_id = pkms.create_note(
    "Python Loops",
    tags=["python", "programming"],
    content="For loops iterate over sequences. While loops continue until a condition is false."
)
note2_id = pkms.create_note(
    "Python Functions",
    tags=["python", "programming"],
    content="Functions are reusable blocks of code defined with def keyword."
)
print(f"   Created notes: #{note1_id}, #{note2_id}")

print("3. Creating test task...")
task_id = task_manager.create_task(
    "Study Python basics",
    priority=4,
    due_date="2025-11-20"
)
print(f"   Created task: #{task_id}")

# Test each AI agent
print("\n" + "-"*70)
print("Testing AI Agents (this will make API calls)...")
print("-"*70 + "\n")

try:
    # Test 1: Summary Generator
    print("🤖 Test 1: AI Summary Generator")
    summary_gen = SummaryGenerator(pkms)
    summary = summary_gen.generate_summary(note1_id)
    print(f"   ✓ Generated summary: {summary[:60]}...")
    
    # Test 2: Tag Suggester
    print("\n🤖 Test 2: AI Tag Suggester")
    tag_suggester = TagSuggester(pkms)
    tags = tag_suggester.suggest_tags(note1_id)
    print(f"   ✓ Suggested tags: {', '.join(tags)}")
    
    # Test 3: Link Suggester
    print("\n🤖 Test 3: AI Link Suggester")
    link_suggester = LinkSuggester(pkms)
    links = link_suggester.suggest_links(note1_id)
    if links:
        print(f"   ✓ Found {len(links)} link suggestion(s)")
        if 'reason' in links[0]:
            print(f"   Reason: {links[0]['reason'][:60]}...")
    else:
        print("   ✓ No links suggested (expected with only 2 notes)")
    
    # Test 4: Semantic Search
    print("\n🤖 Test 4: AI Semantic Search")
    search_agent = SemanticSearchAgent(pkms)
    results = search_agent.semantic_search("iteration and repetition")
    print(f"   ✓ Found {len(results)} semantic search result(s)")
    
    # Test 5: Study Planner
    print("\n🤖 Test 5: AI Study Planner")
    planner = StudyPlanner(task_manager, pkms)
    daily = planner.suggest_daily_schedule()
    print(f"   ✓ Generated daily schedule with {len(daily)} task(s)")
    
    # Test 6: Quiz Generator
    print("\n🤖 Test 6: AI Quiz Generator")
    quiz_gen = QuizGenerator(pkms)
    questions = quiz_gen.generate_quiz(note1_id, num_questions=2)
    print(f"   ✓ Generated {len(questions)} quiz question(s)")
    
    # Test 7: Knowledge Assistant
    print("\n🤖 Test 7: AI Knowledge Assistant")
    assistant = KnowledgeAssistant(pkms, task_manager)
    answer = assistant.ask("What programming topics do I have notes on?")
    print(f"   ✓ Generated answer: {answer[:60]}...")
    
    # Test 8: Note Expander
    print("\n🤖 Test 8: AI Note Expander")
    expander = NoteExpander(pkms)
    expanded = expander.expand_note(note1_id, "clarify")
    print(f"   ✓ Generated expanded content: {expanded[:60]}...")
    
    print("\n" + "="*70)
    print("✅ ALL AI FEATURES WORKING CORRECTLY!")
    print("="*70)
    print("\nAll agents successfully initialized and tested.")
    print("You can now use all AI-powered commands in StudyPal.")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nSomething went wrong with the AI features.")
    print("Please check:")
    print("1. Your OpenAI API key is valid")
    print("2. You have internet connection")
    print("3. Your API key has available credits")
    sys.exit(1)

finally:
    # Cleanup test data
    print("\nCleaning up test data...")
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    print("✓ Cleanup complete")
