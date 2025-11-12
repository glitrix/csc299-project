"""Command-line interface for StudyPal."""

import sys
import shlex
from typing import List, Optional
from .storage import Storage
from .pkms import PKMS
from .tasks import TaskManager
from .agents import (LinkSuggester, TagSuggester, StudyPlanner, SummaryGenerator,
                      SemanticSearchAgent, QuizGenerator, KnowledgeAssistant, NoteExpander)
from .utils import parse_tags, format_date, truncate_text, wrap_text


class CLI:
    """Command-line interface for StudyPal."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize CLI with storage and managers.
        
        Args:
            data_dir: Directory for data storage
        """
        self.storage = Storage(data_dir)
        self.pkms = PKMS(self.storage)
        self.task_manager = TaskManager(self.storage)
        
        # Initialize agents
        self.link_suggester = LinkSuggester(self.pkms)
        self.tag_suggester = TagSuggester(self.pkms)
        self.study_planner = StudyPlanner(self.task_manager, self.pkms)
        self.summary_generator = SummaryGenerator(self.pkms)
        self.semantic_search = SemanticSearchAgent(self.pkms)
        self.quiz_generator = QuizGenerator(self.pkms)
        self.knowledge_assistant = KnowledgeAssistant(self.pkms, self.task_manager)
        self.note_expander = NoteExpander(self.pkms)
        
        self.running = True
    
    def run(self):
        """Main command loop."""
        print("Welcome to StudyPal!")
        print("Type 'help' for available commands or 'exit' to quit.\n")
        
        while self.running:
            try:
                command = input("studypal> ").strip()
                if command:
                    self.process_command(command)
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to close StudyPal.")
            except Exception as e:
                print(f"Error: {e}")
    
    def process_command(self, command: str):
        """Process a command string.
        
        Args:
            command: Command string to process
        """
        try:
            parts = shlex.split(command)
        except ValueError as e:
            print(f"Error parsing command: {e}")
            return
        
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Command routing
        if cmd in ["exit", "quit"]:
            self.cmd_exit(args)
        elif cmd == "help":
            self.cmd_help(args)
        elif cmd == "add":
            self.cmd_add(args)
        elif cmd == "list":
            self.cmd_list(args)
        elif cmd == "show":
            self.cmd_show(args)
        elif cmd == "update":
            self.cmd_update(args)
        elif cmd == "delete":
            self.cmd_delete(args)
        elif cmd == "search":
            self.cmd_search(args)
        elif cmd == "link":
            self.cmd_link(args)
        elif cmd == "suggest":
            self.cmd_suggest(args)
        elif cmd == "plan":
            self.cmd_plan(args)
        elif cmd == "summary":
            self.cmd_summary(args)
        elif cmd == "stats":
            self.cmd_stats(args)
        elif cmd == "ask":
            self.cmd_ask(args)
        elif cmd == "quiz":
            self.cmd_quiz(args)
        elif cmd == "expand":
            self.cmd_expand(args)
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")
    
    def cmd_exit(self, args: List[str]):
        """Exit the application."""
        print("Goodbye!")
        self.running = False
    
    def cmd_help(self, args: List[str]):
        """Display help information."""
        help_text = """
Available commands:

NOTES:
  add note "Title" [--tags tag1,tag2] [--content "content"]
      Create a new note
  list notes [--tag tagname]
      List all notes or notes with a specific tag
  show note <id>
      Display a specific note
  search notes "keyword"
      Search for notes containing a keyword
  update note <id> [--title "New Title"] [--content "content"] [--tags tag1,tag2]
      Update a note
  delete note <id>
      Delete a note
  link note <id1> to <id2> [--type related]
      Create a link between two notes

TASKS:
  add task "Title" [--due YYYY-MM-DD] [--priority 1-5] [--desc "description"]
      Create a new task
  list tasks [--status todo|in_progress|done] [--priority 1-5]
      List all tasks or filtered tasks
  show task <id>
      Display a specific task
  update task <id> [--title "New Title"] [--status todo|in_progress|done] 
                    [--priority 1-5] [--due YYYY-MM-DD]
      Update a task
  delete task <id>
      Delete a task
  stats
      Show task statistics

AI AGENTS (All use OpenAI API):
  suggest links <note_id>
      AI-powered semantic link suggestions between notes
  suggest tags <note_id>
      AI-generated contextually relevant tags
  plan week
      Generate an intelligent weekly study plan
  plan today
      Get AI-recommended tasks for today
  summary <note_id>
      Generate AI-powered note summary
  search notes "natural language query"
      Semantic search - find notes by meaning
  ask "your question"
      Ask questions about your notes and tasks
  quiz <note_id> [--num 5]
      Generate quiz questions from a note
  expand <note_id> [--mode expand|clarify|examples|simplify]
      AI-assisted note improvement

GENERAL:
  help
      Show this help message
  exit or quit
      Close StudyPal
"""
        print(help_text)
    
    def cmd_add(self, args: List[str]):
        """Handle add commands."""
        if not args:
            print("Usage: add note|task ...")
            return
        
        entity_type = args[0].lower()
        
        if entity_type == "note":
            self._add_note(args[1:])
        elif entity_type == "task":
            self._add_task(args[1:])
        else:
            print(f"Unknown entity type: {entity_type}")
    
    def _add_note(self, args: List[str]):
        """Add a new note."""
        if not args:
            print("Usage: add note \"Title\" [--tags tag1,tag2] [--content \"content\"]")
            return
        
        title = args[0]
        tags = []
        content = ""
        
        i = 1
        while i < len(args):
            if args[i] == "--tags" and i + 1 < len(args):
                tags = parse_tags(args[i + 1])
                i += 2
            elif args[i] == "--content" and i + 1 < len(args):
                content = args[i + 1]
                i += 2
            else:
                i += 1
        
        note_id = self.pkms.add_note(title, content, tags)
        print(f"Created note #{note_id}: {title}")
        if tags:
            print(f"Tags: {', '.join(tags)}")
    
    def _add_task(self, args: List[str]):
        """Add a new task."""
        if not args:
            print("Usage: add task \"Title\" [--due YYYY-MM-DD] [--priority 1-5] [--desc \"description\"]")
            return
        
        title = args[0]
        due_date = None
        priority = 2
        description = ""
        
        i = 1
        while i < len(args):
            if args[i] == "--due" and i + 1 < len(args):
                due_date = args[i + 1]
                i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                try:
                    priority = int(args[i + 1])
                except ValueError:
                    print(f"Invalid priority: {args[i + 1]}")
                    return
                i += 2
            elif args[i] == "--desc" and i + 1 < len(args):
                description = args[i + 1]
                i += 2
            else:
                i += 1
        
        try:
            task_id = self.task_manager.add_task(title, description, priority, due_date)
            print(f"Created task #{task_id}: {title}")
            if due_date:
                print(f"Due: {due_date}")
            print(f"Priority: {priority}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def cmd_list(self, args: List[str]):
        """Handle list commands."""
        if not args:
            print("Usage: list notes|tasks [options]")
            return
        
        entity_type = args[0].lower()
        
        if entity_type == "notes":
            self._list_notes(args[1:])
        elif entity_type == "tasks":
            self._list_tasks(args[1:])
        else:
            print(f"Unknown entity type: {entity_type}")
    
    def _list_notes(self, args: List[str]):
        """List all notes."""
        tag = None
        
        i = 0
        while i < len(args):
            if args[i] == "--tag" and i + 1 < len(args):
                tag = args[i + 1]
                i += 2
            else:
                i += 1
        
        notes = self.pkms.list_notes(tag=tag)
        
        if not notes:
            print("No notes found.")
            return
        
        print(f"\nFound {len(notes)} note(s):")
        print("-" * 70)
        for note in notes:
            tags_str = f"[{', '.join(note.get('tags', []))}]" if note.get('tags') else ""
            content_preview = truncate_text(note.get('content', ''), 40)
            print(f"#{note['id']}: {note['title']} {tags_str}")
            if content_preview:
                print(f"    {content_preview}")
        print("-" * 70)
    
    def _list_tasks(self, args: List[str]):
        """List all tasks."""
        status = None
        priority = None
        
        i = 0
        while i < len(args):
            if args[i] == "--status" and i + 1 < len(args):
                status = args[i + 1]
                i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                try:
                    priority = int(args[i + 1])
                except ValueError:
                    print(f"Invalid priority: {args[i + 1]}")
                    return
                i += 2
            else:
                i += 1
        
        tasks = self.task_manager.list_tasks(status=status, priority=priority)
        
        if not tasks:
            print("No tasks found.")
            return
        
        print(f"\nFound {len(tasks)} task(s):")
        print("-" * 70)
        for task in tasks:
            status_marker = {
                "todo": "[ ]",
                "in_progress": "[~]",
                "done": "[✓]"
            }.get(task['status'], "[ ]")
            
            due_str = f"(due: {task['due_date']})" if task.get('due_date') else ""
            print(f"{status_marker} #{task['id']}: {task['title']} [P{task['priority']}] {due_str}")
        print("-" * 70)
    
    def cmd_show(self, args: List[str]):
        """Handle show commands."""
        if len(args) < 2:
            print("Usage: show note|task <id>")
            return
        
        entity_type = args[0].lower()
        try:
            entity_id = int(args[1])
        except ValueError:
            print(f"Invalid ID: {args[1]}")
            return
        
        if entity_type == "note":
            self._show_note(entity_id)
        elif entity_type == "task":
            self._show_task(entity_id)
        else:
            print(f"Unknown entity type: {entity_type}")
    
    def _show_note(self, note_id: int):
        """Display a specific note."""
        note = self.pkms.get_note(note_id)
        if not note:
            print(f"Note #{note_id} not found.")
            return
        
        print("\n" + "=" * 70)
        print(f"Note #{note['id']}: {note['title']}")
        print("=" * 70)
        if note.get('tags'):
            print(f"Tags: {', '.join(note['tags'])}")
        print(f"Created: {format_date(note['created_at'])}")
        print(f"Updated: {format_date(note['updated_at'])}")
        print("-" * 70)
        print(note.get('content', '(No content)'))
        print("=" * 70)
        
        # Show linked notes
        linked = self.pkms.get_linked_notes(note_id)
        if linked:
            print(f"\nLinked notes ({len(linked)}):")
            for linked_note in linked:
                direction = "→" if linked_note['link_direction'] == 'outgoing' else "←"
                print(f"  {direction} #{linked_note['id']}: {linked_note['title']}")
    
    def _show_task(self, task_id: int):
        """Display a specific task."""
        task = self.task_manager.get_task(task_id)
        if not task:
            print(f"Task #{task_id} not found.")
            return
        
        print("\n" + "=" * 70)
        print(f"Task #{task['id']}: {task['title']}")
        print("=" * 70)
        print(f"Status: {task['status']}")
        print(f"Priority: {task['priority']}")
        if task.get('due_date'):
            print(f"Due: {task['due_date']}")
        print(f"Created: {format_date(task['created_at'])}")
        print(f"Updated: {format_date(task['updated_at'])}")
        if task.get('description'):
            print("-" * 70)
            print(task['description'])
        print("=" * 70)
    
    def cmd_update(self, args: List[str]):
        """Handle update commands."""
        if len(args) < 2:
            print("Usage: update note|task <id> [options]")
            return
        
        entity_type = args[0].lower()
        try:
            entity_id = int(args[1])
        except ValueError:
            print(f"Invalid ID: {args[1]}")
            return
        
        if entity_type == "note":
            self._update_note(entity_id, args[2:])
        elif entity_type == "task":
            self._update_task(entity_id, args[2:])
        else:
            print(f"Unknown entity type: {entity_type}")
    
    def _update_note(self, note_id: int, args: List[str]):
        """Update a note."""
        title = None
        content = None
        tags = None
        
        i = 0
        while i < len(args):
            if args[i] == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            elif args[i] == "--content" and i + 1 < len(args):
                content = args[i + 1]
                i += 2
            elif args[i] == "--tags" and i + 1 < len(args):
                tags = parse_tags(args[i + 1])
                i += 2
            else:
                i += 1
        
        success = self.pkms.update_note(note_id, title, content, tags)
        if success:
            print(f"Updated note #{note_id}")
        else:
            print(f"Note #{note_id} not found.")
    
    def _update_task(self, task_id: int, args: List[str]):
        """Update a task."""
        title = None
        status = None
        priority = None
        due_date = None
        description = None
        
        i = 0
        while i < len(args):
            if args[i] == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            elif args[i] == "--status" and i + 1 < len(args):
                status = args[i + 1]
                i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                try:
                    priority = int(args[i + 1])
                except ValueError:
                    print(f"Invalid priority: {args[i + 1]}")
                    return
                i += 2
            elif args[i] == "--due" and i + 1 < len(args):
                due_date = args[i + 1]
                i += 2
            elif args[i] == "--desc" and i + 1 < len(args):
                description = args[i + 1]
                i += 2
            else:
                i += 1
        
        try:
            success = self.task_manager.update_task(task_id, title, description, 
                                                   status, priority, due_date)
            if success:
                print(f"Updated task #{task_id}")
            else:
                print(f"Task #{task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def cmd_delete(self, args: List[str]):
        """Handle delete commands."""
        if len(args) < 2:
            print("Usage: delete note|task <id>")
            return
        
        entity_type = args[0].lower()
        try:
            entity_id = int(args[1])
        except ValueError:
            print(f"Invalid ID: {args[1]}")
            return
        
        if entity_type == "note":
            success = self.pkms.delete_note(entity_id)
            if success:
                print(f"Deleted note #{entity_id}")
            else:
                print(f"Note #{entity_id} not found.")
        elif entity_type == "task":
            success = self.task_manager.delete_task(entity_id)
            if success:
                print(f"Deleted task #{entity_id}")
            else:
                print(f"Task #{entity_id} not found.")
        else:
            print(f"Unknown entity type: {entity_type}")
    
    def cmd_search(self, args: List[str]):
        """Handle search commands with AI semantic search."""
        if len(args) < 2:
            print("Usage: search notes \"keyword or natural language query\"")
            return
        
        entity_type = args[0].lower()
        query = args[1]
        
        if entity_type == "notes":
            # First try keyword search
            keyword_results = self.pkms.search_notes(query)
            
            # Then try semantic search with AI
            print(f"\n🔍 Performing AI-powered semantic search for: '{query}'...")
            try:
                semantic_results = self.semantic_search.semantic_search(query)
                
                if semantic_results:
                    print("\n✨ AI Semantic Search Results:")
                    print("=" * 70)
                    for result in semantic_results:
                        note = result['note']
                        reason = result['relevance']
                        tags_str = f"[{', '.join(note.get('tags', []))}]" if note.get('tags') else ""
                        print(f"\n#{note['id']}: {note['title']} {tags_str}")
                        print(f"  💡 AI Response: {reason}")
                    print("=" * 70)
                elif keyword_results:
                    print("\nNo semantic matches, showing keyword results:")
                    print("-" * 70)
                    for note in keyword_results:
                        tags_str = f"[{', '.join(note.get('tags', []))}]" if note.get('tags') else ""
                        print(f"#{note['id']}: {note['title']} {tags_str}")
                    print("-" * 70)
                else:
                    print(f"No notes found matching '{query}'.")
            except Exception as e:
                # Fallback to keyword search on error
                if keyword_results:
                    print("\n(AI search unavailable, showing keyword results)")
                    print("-" * 70)
                    for note in keyword_results:
                        tags_str = f"[{', '.join(note.get('tags', []))}]" if note.get('tags') else ""
                        print(f"#{note['id']}: {note['title']} {tags_str}")
                    print("-" * 70)
                else:
                    print(f"No notes found matching '{query}'.")
        else:
            print(f"Search not supported for: {entity_type}")
    
    def cmd_link(self, args: List[str]):
        """Handle link command."""
        if len(args) < 4 or args[0] != "note" or args[2] != "to":
            print("Usage: link note <id1> to <id2> [--type related]")
            return
        
        try:
            from_id = int(args[1])
            to_id = int(args[3])
        except ValueError:
            print("Invalid note IDs.")
            return
        
        link_type = "related"
        if len(args) > 5 and args[4] == "--type":
            link_type = args[5]
        
        success = self.pkms.link_notes(from_id, to_id, link_type)
        if success:
            print(f"Linked note #{from_id} to note #{to_id} ({link_type})")
        else:
            print("Failed to create link. Check that both notes exist.")
    
    def cmd_suggest(self, args: List[str]):
        """Handle suggest commands."""
        if len(args) < 2:
            print("Usage: suggest links|tags <id>")
            return
        
        suggestion_type = args[0].lower()
        
        try:
            entity_id = int(args[1])
        except ValueError:
            print(f"Invalid ID: {args[1]}")
            return
        
        if suggestion_type == "links":
            suggestions = self.link_suggester.suggest_links(entity_id)
            if not suggestions:
                print(f"No link suggestions found for note #{entity_id}.")
                return
            
            print(f"\n✨ AI-Powered Link Suggestions for note #{entity_id}:")
            print("=" * 70)
            for suggestion in suggestions:
                note = suggestion['note']
                tags_str = f"[{', '.join(note.get('tags', []))}]" if note.get('tags') else ""
                print(f"\n#{note['id']}: {note['title']} {tags_str}")
                if 'reason' in suggestion:
                    print(f"  💡 AI Response: {suggestion['reason']}")
            print("=" * 70)
        
        elif suggestion_type == "tags":
            suggestions = self.tag_suggester.suggest_tags(entity_id)
            if not suggestions:
                print(f"No tag suggestions found for note #{entity_id}.")
                return
            
            print(f"\nAI Response - Suggested tags for note #{entity_id}:")
            print(", ".join(suggestions))
        
        else:
            print(f"Unknown suggestion type: {suggestion_type}")
    
    def cmd_plan(self, args: List[str]):
        """Handle plan commands."""
        if not args:
            print("Usage: plan week|today")
            return
        
        plan_type = args[0].lower()
        
        if plan_type == "week":
            plan = self.study_planner.plan_week()
            print("\nAI Response - Weekly Study Plan:")
            print("=" * 70)
            for day, activities in plan.items():
                print(f"\n{day}:")
                if not activities:
                    print("  (Rest day)")
                    continue
                
                for activity in activities:
                    if activity['type'] == 'task':
                        task = activity['task']
                        print(f"  • {task['title']} ({activity['estimated_hours']}h) [P{task['priority']}]")
                    elif activity['type'] == 'review':
                        note = activity['note']
                        print(f"  • Review: {note['title']} ({activity['estimated_hours']}h)")
            print("=" * 70)
        
        elif plan_type == "today":
            tasks = self.study_planner.suggest_daily_schedule()
            if not tasks:
                print("No tasks recommended for today!")
                return
            
            print("\nAI Response - Recommended tasks for today:")
            print("-" * 70)
            for task in tasks:
                due_str = f"(due: {task['due_date']})" if task.get('due_date') else ""
                print(f"#{task['id']}: {task['title']} [P{task['priority']}] {due_str}")
            print("-" * 70)
        
        else:
            print(f"Unknown plan type: {plan_type}")
    
    def cmd_summary(self, args: List[str]):
        """Handle summary command."""
        if not args:
            print("Usage: summary <note_id>")
            return
        
        try:
            note_id = int(args[0])
        except ValueError:
            print(f"Invalid ID: {args[0]}")
            return
        
        summary = self.summary_generator.generate_summary(note_id)
        print(f"\nAI Response - Summary of note #{note_id}:")
        print("-" * 70)
        print(wrap_text(summary))
        print("-" * 70)
    
    def cmd_stats(self, args: List[str]):
        """Display task statistics."""
        stats = self.task_manager.get_statistics()
        
        print("\nTask Statistics:")
        print("=" * 70)
        print(f"Total tasks: {stats['total']}")
        print(f"  • To do: {stats['todo']}")
        print(f"  • In progress: {stats['in_progress']}")
        print(f"  • Completed: {stats['done']}")
        print(f"\nOverdue: {stats['overdue']}")
        print(f"Due this week: {stats['due_this_week']}")
        print(f"Completion rate: {stats['completion_rate']:.1f}%")
        print("=" * 70)
    
    def cmd_ask(self, args: List[str]):
        """Handle ask command - answer questions about notes and tasks."""
        if not args:
            print("Usage: ask \"your question\"")
            return
        
        question = ' '.join(args)
        print(f"\n💭 Thinking about: {question}\n")
        
        try:
            answer = self.knowledge_assistant.ask(question)
            print("🤖 AI Response:")
            print("=" * 70)
            print(wrap_text(answer))
            print("=" * 70)
        except Exception as e:
            print(f"Sorry, I couldn't answer that question. Error: {e}")
    
    def cmd_quiz(self, args: List[str]):
        """Handle quiz command - generate quiz questions from a note."""
        if not args:
            print("Usage: quiz <note_id> [--num 5]")
            return
        
        try:
            note_id = int(args[0])
        except ValueError:
            print(f"Invalid note ID: {args[0]}")
            return
        
        num_questions = 5
        if len(args) > 2 and args[1] == "--num":
            try:
                num_questions = int(args[2])
            except ValueError:
                pass
        
        print(f"\n📝 Generating {num_questions} quiz questions...\n")
        
        try:
            questions = self.quiz_generator.generate_quiz(note_id, num_questions)
            
            if not questions:
                print("Could not generate questions for this note.")
                return
            
            print("AI Response - Quiz Questions:")
            print("=" * 70)
            for i, q in enumerate(questions, 1):
                print(f"\nQ{i}: {q.get('question', 'N/A')}")
                print(f"Type: {q.get('type', 'N/A')}")
                if q.get('options'):
                    print(f"Options: {q['options']}")
                print(f"Answer: {q.get('answer', 'N/A')}")
                print("-" * 70)
        except Exception as e:
            print(f"Error generating quiz: {e}")
    
    def cmd_expand(self, args: List[str]):
        """Handle expand command - AI-assisted note improvement."""
        if not args:
            print("Usage: expand <note_id> [--mode expand|clarify|examples|simplify]")
            return
        
        try:
            note_id = int(args[0])
        except ValueError:
            print(f"Invalid note ID: {args[0]}")
            return
        
        mode = "expand"
        if len(args) > 2 and args[1] == "--mode":
            mode = args[2]
        
        print(f"\n✨ Improving note #{note_id} (mode: {mode})...\n")
        
        try:
            improved_content = self.note_expander.expand_note(note_id, mode)
            
            print("AI Response - Improved Content:")
            print("=" * 70)
            print(wrap_text(improved_content))
            print("=" * 70)
            print("\nTo save this, use: update note <id> --content \"<paste content>\"")
        except Exception as e:
            print(f"Error improving note: {e}")
