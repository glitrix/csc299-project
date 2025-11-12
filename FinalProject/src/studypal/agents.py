"""AI Agents module for StudyPal - provides intelligent assistance."""

import os
import sys
from typing import List, Dict, Optional
from collections import Counter
import re
from datetime import datetime, timedelta
from .storage import Storage
from .pkms import PKMS
from .tasks import TaskManager

# OpenAI integration - REQUIRED
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: OpenAI package is required but not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class LinkSuggester:
    """Agent that suggests links between notes using AI semantic analysis."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance to analyze notes
        """
        self.pkms = pkms
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered link suggestions will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def _extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """Extract meaningful keywords from text.
        
        Args:
            text: Text to extract keywords from
            min_length: Minimum word length to consider
            
        Returns:
            List of keywords
        """
        # Remove special characters and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out short words and common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                      'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 
                      'was', 'were', 'be', 'been', 'being', 'this', 'that'}
        
        keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
        return keywords
    
    def _calculate_similarity(self, note1: Dict, note2: Dict) -> float:
        """Calculate similarity score between two notes.
        
        Args:
            note1: First note dictionary
            note2: Second note dictionary
            
        Returns:
            Similarity score between 0 and 1
        """
        # Combine title and content for analysis
        text1 = f"{note1['title']} {note1.get('content', '')}"
        text2 = f"{note2['title']} {note2.get('content', '')}"
        
        keywords1 = set(self._extract_keywords(text1))
        keywords2 = set(self._extract_keywords(text2))
        
        # Calculate Jaccard similarity
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)
        
        similarity = len(intersection) / len(union) if union else 0.0
        
        # Boost similarity if they share tags
        tags1 = set(note1.get('tags', []))
        tags2 = set(note2.get('tags', []))
        shared_tags = tags1.intersection(tags2)
        
        if shared_tags:
            similarity = min(1.0, similarity + 0.2 * len(shared_tags))
        
        return similarity
    
    def suggest_links(self, note_id: int, min_similarity: float = 0.15, 
                      max_suggestions: int = 5) -> List[Dict]:
        """Suggest notes that might be related using AI semantic analysis.
        
        Args:
            note_id: ID of the note to find links for
            min_similarity: Minimum similarity threshold (ignored for AI)
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of suggested notes with reasons
        """
        target_note = self.pkms.get_note(note_id)
        if not target_note:
            return []
        
        all_notes = self.pkms.list_notes()
        
        # Get existing links to avoid suggesting them
        existing_links = self.pkms.get_linked_notes(note_id)
        existing_ids = {note['id'] for note in existing_links}
        
        # Filter candidates
        candidate_notes = [n for n in all_notes 
                          if n['id'] != note_id and n['id'] not in existing_ids]
        
        if not candidate_notes:
            return []
        
        # Use AI for semantic link suggestions
        try:
            return self._suggest_links_with_ai(target_note, candidate_notes, max_suggestions)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Falling back to keyword-based suggestions...")
            # Fallback to simple method
            suggestions = []
            for note in candidate_notes:
                similarity = self._calculate_similarity(target_note, note)
                if similarity >= min_similarity:
                    suggestions.append({
                        'note': note,
                        'similarity': similarity,
                        'reason': 'Keyword-based similarity'
                    })
            suggestions.sort(key=lambda x: x['similarity'], reverse=True)
            return suggestions[:max_suggestions]
    
    def _suggest_links_with_ai(self, target_note: Dict, candidates: List[Dict], max_suggestions: int) -> List[Dict]:
        """Use AI to find semantic relationships between notes.
        
        Args:
            target_note: The note to find links for
            candidates: List of candidate notes
            max_suggestions: Maximum suggestions to return
            
        Returns:
            List of suggested links with AI-generated reasons
        """
        # Prepare target note info
        target_info = f"Title: {target_note['title']}\n"
        target_info += f"Tags: {', '.join(target_note.get('tags', []))}\n"
        target_info += f"Content: {target_note.get('content', '')[:500]}"  # Limit content length
        
        # Prepare candidate info (limit to top 10 to avoid token limits)
        candidate_info = []
        for i, note in enumerate(candidates[:10]):
            info = f"\n{i+1}. ID {note['id']}: {note['title']}"
            if note.get('tags'):
                info += f" [Tags: {', '.join(note['tags'])}]"
            if note.get('content'):
                info += f"\n   Content preview: {note['content'][:200]}..."
            candidate_info.append(info)
        
        prompt = f"""Analyze these notes and suggest which ones should be linked to the target note.
Consider semantic relationships, shared concepts, prerequisite knowledge, or complementary topics.

TARGET NOTE:
{target_info}

CANDIDATE NOTES:
{''.join(candidate_info)}

Respond with up to {max_suggestions} suggestions in this format:
ID X - Brief reason why they should be linked
ID Y - Brief reason why they should be linked

Only suggest notes with meaningful conceptual connections."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a knowledge management assistant that identifies semantic relationships between study notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=400
        )
        
        ai_response = response.choices[0].message.content
        
        # Parse AI response
        suggestions = []
        note_dict = {note['id']: note for note in candidates}
        
        for line in ai_response.split('\n'):
            match = re.search(r'ID\s+(\d+)\s*-\s*(.+)', line)
            if match:
                note_id = int(match.group(1))
                reason = match.group(2).strip()
                
                if note_id in note_dict:
                    suggestions.append({
                        'note': note_dict[note_id],
                        'similarity': 0.9,  # High score for AI suggestions
                        'reason': reason
                    })
        
        return suggestions[:max_suggestions]


class TagSuggester:
    """Agent that suggests tags for notes using AI content analysis."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance to analyze notes
        """
        self.pkms = pkms
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered tag suggestions will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def suggest_tags(self, note_id: int, max_suggestions: int = 5) -> List[str]:
        """Suggest tags for a note using AI content analysis.
        
        Args:
            note_id: ID of the note
            max_suggestions: Maximum number of tag suggestions
            
        Returns:
            List of suggested tag strings
        """
        note = self.pkms.get_note(note_id)
        if not note:
            return []
        
        # Use AI for intelligent tag suggestions
        try:
            return self._suggest_tags_with_ai(note, max_suggestions)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _suggest_tags_with_ai(self, note: Dict, max_suggestions: int) -> List[str]:
        """Use AI to suggest contextually relevant tags.
        
        Args:
            note: Note dictionary
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of suggested tags
        """
        # Get existing tags in the system for context
        all_tags = self.pkms.get_all_tags()
        current_tags = note.get('tags', [])
        
        # Prepare note info
        title = note['title']
        content = note.get('content', '')[:800]  # Limit content length
        
        existing_tags_str = ', '.join(all_tags[:20]) if all_tags else 'None yet'
        current_tags_str = ', '.join(current_tags) if current_tags else 'None'
        
        prompt = f"""Suggest {max_suggestions} relevant tags for this study note.
Consider the topic, key concepts, and relationships to existing tags.
Tags should be concise (1-2 words) and useful for organization.

Note Title: {title}
Current Tags: {current_tags_str}
Content:
{content}

Existing tags in the system: {existing_tags_str}

Respond with just the tag names, one per line. Prefer existing tags when appropriate, but suggest new ones if needed."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests relevant, concise tags for study notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content
        
        # Parse tags from response
        suggested_tags = []
        for line in ai_response.split('\n'):
            line = line.strip().strip('-•*').strip()
            if line and line not in current_tags:
                suggested_tags.append(line)
        
        return suggested_tags[:max_suggestions]


class StudyPlanner:
    """Agent that creates study plans based on tasks and priorities."""
    
    def __init__(self, task_manager: TaskManager, pkms: PKMS):
        """Initialize with TaskManager and PKMS instances.
        
        Args:
            task_manager: TaskManager instance
            pkms: PKMS instance
        """
        self.task_manager = task_manager
        self.pkms = pkms
        
        # Initialize OpenAI client - REQUIRED
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nERROR: OPENAI_API_KEY environment variable is not set!")
            print("Please set your OpenAI API key in the .env file.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def plan_week(self) -> Dict[str, List[Dict]]:
        """Create a weekly study plan based on tasks and deadlines using AI.
        
        Returns:
            Dictionary mapping day names to lists of planned activities
        """
        # Get all incomplete tasks
        todo_tasks = self.task_manager.list_tasks(status="todo")
        in_progress = self.task_manager.list_tasks(status="in_progress")
        all_tasks = todo_tasks + in_progress
        
        if not all_tasks:
            # No tasks to plan
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            return {day: [] for day in days}
        
        # Always use AI planning
        try:
            return self._plan_week_with_ai(all_tasks)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _plan_week_with_ai(self, all_tasks: List[Dict]) -> Dict[str, List[Dict]]:
        """Create weekly plan using OpenAI for intelligent scheduling.
        
        Args:
            all_tasks: List of tasks to plan
            
        Returns:
            Dictionary mapping day names to lists of planned activities
        """
        # Prepare task information for AI
        task_info = []
        for task in all_tasks:
            info = f"Task: {task['title']}, Priority: {task.get('priority', 1)}"
            if task.get('due_date'):
                info += f", Due: {task['due_date']}"
            if task.get('description'):
                info += f", Description: {task['description']}"
            task_info.append(info)
        
        # Get notes for context
        notes = self.pkms.list_notes()
        note_titles = [note['title'] for note in notes[:10]]  # Limit to 10 notes
        
        # Create prompt for AI
        prompt = f"""Create an optimal weekly study plan for the following tasks and notes.
        
Tasks to schedule:
{chr(10).join(task_info)}

Available study notes: {', '.join(note_titles) if note_titles else 'None'}

Please create a balanced weekly schedule (Monday-Sunday) that:
1. Prioritizes tasks by priority and due date
2. Distributes workload evenly across the week
3. Estimates study hours for each task (1-3 hours based on priority)
4. Includes note review sessions on lighter days
5. Keeps weekdays busier than weekends

Respond in this exact format:
Monday:
- Task Name (Xh) [Priority]
Tuesday:
- Task Name (Xh) [Priority]
...

Keep it concise and practical."""

        # Call OpenAI API
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study planning assistant. Create practical, balanced study schedules."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        ai_plan_text = response.choices[0].message.content
        
        # Parse AI response into structured plan
        return self._parse_ai_plan(ai_plan_text, all_tasks, notes)
    
    def _parse_ai_plan(self, ai_text: str, tasks: List[Dict], notes: List[Dict]) -> Dict[str, List[Dict]]:
        """Parse AI-generated plan text into structured format.
        
        Args:
            ai_text: AI-generated plan text
            tasks: List of all tasks
            notes: List of all notes
            
        Returns:
            Structured plan dictionary
        """
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        plan = {day: [] for day in days}
        
        current_day = None
        lines = ai_text.split('\n')
        
        # Create task lookup by title
        task_lookup = {task['title'].lower(): task for task in tasks}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a day header
            for day in days:
                if day in line and ':' in line:
                    current_day = day
                    break
            
            # Parse task/activity lines
            if current_day and line.startswith('-'):
                # Try to extract task info
                # Look for patterns like "Task Name (2h) [P4]"
                task_match = re.search(r'-\s*(.+?)\s*\((\d+(?:\.\d+)?)h\)', line)
                if task_match:
                    task_name = task_match.group(1).strip()
                    hours = float(task_match.group(2))
                    
                    # Try to find matching task
                    task_name_lower = task_name.lower().replace('[', '').replace(']', '').strip()
                    for title, task in task_lookup.items():
                        if title in task_name_lower or task_name_lower in title:
                            plan[current_day].append({
                                'task': task,
                                'estimated_hours': hours,
                                'type': 'task'
                            })
                            break
        
        # If parsing failed, raise error
        if all(len(activities) == 0 for activities in plan.values()):
            raise ValueError("Failed to parse AI-generated plan. Please try again.")
        
        return plan
    
    def suggest_daily_schedule(self) -> List[Dict]:
        """Suggest tasks for today using AI-powered prioritization.
        
        Returns:
            List of tasks recommended for today
        """
        # Get tasks due soon
        due_soon = self.task_manager.get_tasks_due_soon(days=1)
        
        # Get high priority tasks
        high_priority = self.task_manager.get_tasks_by_priority(5)
        high_priority.extend(self.task_manager.get_tasks_by_priority(4))
        
        # Combine and deduplicate
        task_ids = set()
        daily_tasks = []
        
        for task in due_soon + high_priority:
            if task['id'] not in task_ids and task['status'] != 'done':
                task_ids.add(task['id'])
                daily_tasks.append(task)
        
        if not daily_tasks:
            return []
        
        # Always use AI recommendations
        try:
            return self._suggest_daily_with_ai(daily_tasks)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _suggest_daily_with_ai(self, tasks: List[Dict]) -> List[Dict]:
        """Use AI to suggest optimal daily schedule.
        
        Args:
            tasks: List of candidate tasks
            
        Returns:
            Ordered list of recommended tasks
        """
        # Prepare task information
        task_info = []
        for task in tasks:
            info = f"ID {task['id']}: {task['title']}, Priority: {task.get('priority', 1)}"
            if task.get('due_date'):
                info += f", Due: {task['due_date']}"
            if task.get('description'):
                info += f", Desc: {task['description']}"
            task_info.append(info)
        
        prompt = f"""Given these tasks, recommend the top 5 tasks to focus on today.
Consider priority, due dates, and task descriptions.

Tasks:
{chr(10).join(task_info)}

Respond with task IDs in order of importance, one per line, like:
1. ID X - Brief reason
2. ID Y - Brief reason
..."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a productivity assistant helping prioritize daily tasks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        ai_response = response.choices[0].message.content
        
        # Extract task IDs from AI response
        recommended_ids = []
        for line in ai_response.split('\n'):
            match = re.search(r'ID\s+(\d+)', line)
            if match:
                recommended_ids.append(int(match.group(1)))
        
        # Reorder tasks based on AI recommendations
        task_dict = {task['id']: task for task in tasks}
        recommended_tasks = []
        
        for task_id in recommended_ids:
            if task_id in task_dict:
                recommended_tasks.append(task_dict[task_id])
        
        # Add any remaining tasks
        for task in tasks:
            if task not in recommended_tasks:
                recommended_tasks.append(task)
        
        return recommended_tasks[:5]


class SummaryGenerator:
    """Agent that generates summaries of notes using AI."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance
        """
        self.pkms = pkms
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered summaries will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def generate_summary(self, note_id: int, max_sentences: int = 3) -> str:
        """Generate an AI-powered summary of a note.
        
        Args:
            note_id: ID of the note to summarize
            max_sentences: Maximum number of sentences in summary
            
        Returns:
            Summary text
        """
        note = self.pkms.get_note(note_id)
        if not note:
            return "Note not found."
        
        content = note.get('content', '')
        if not content:
            return f"Note '{note['title']}' has no content."
        
        # Use AI for intelligent summarization
        try:
            return self._generate_ai_summary(note, max_sentences)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _generate_ai_summary(self, note: Dict, max_sentences: int) -> str:
        """Generate summary using OpenAI.
        
        Args:
            note: Note dictionary
            max_sentences: Maximum sentences in summary
            
        Returns:
            AI-generated summary
        """
        title = note['title']
        content = note.get('content', '')
        tags = ', '.join(note.get('tags', []))
        
        prompt = f"""Summarize this study note in {max_sentences} sentences or less.
Focus on the key concepts and main ideas.

Title: {title}
Tags: {tags if tags else 'None'}

Content:
{content}

Provide a clear, concise summary suitable for quick review."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant that creates clear, concise summaries of study notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    def summarize_all_notes(self, tag: Optional[str] = None) -> List[Dict]:
        """Generate summaries for all notes or notes with a specific tag.
        
        Args:
            tag: Optional tag to filter notes by
            
        Returns:
            List of dictionaries with note info and summaries
        """
        notes = self.pkms.list_notes(tag=tag)
        summaries = []
        
        for note in notes:
            summary = self.generate_summary(note['id'])
            summaries.append({
                'id': note['id'],
                'title': note['title'],
                'tags': note.get('tags', []),
                'summary': summary
            })
        
        return summaries


class SemanticSearchAgent:
    """Agent that performs semantic search over notes using AI."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance
        """
        self.pkms = pkms
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered semantic search will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def semantic_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Perform semantic search using natural language query.
        
        Args:
            query: Natural language search query
            max_results: Maximum number of results
            
        Returns:
            List of matching notes with relevance scores
        """
        all_notes = self.pkms.list_notes()
        
        if not all_notes:
            return []
        
        try:
            return self._semantic_search_with_ai(query, all_notes, max_results)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _semantic_search_with_ai(self, query: str, notes: List[Dict], max_results: int) -> List[Dict]:
        """Use AI to find semantically relevant notes.
        
        Args:
            query: Search query
            notes: List of all notes
            max_results: Maximum results to return
            
        Returns:
            List of relevant notes with scores
        """
        # Prepare notes info (limit to 20 for token efficiency)
        notes_info = []
        for note in notes[:20]:
            info = f"\nID {note['id']}: {note['title']}"
            if note.get('tags'):
                info += f" [Tags: {', '.join(note['tags'])}]"
            if note.get('content'):
                info += f"\n  {note['content'][:250]}..."
            notes_info.append(info)
        
        prompt = f"""Find notes that best match this query: "{query}"

Consider semantic meaning, not just keyword matches.

AVAILABLE NOTES:
{''.join(notes_info)}

Respond with up to {max_results} most relevant notes in this format:
ID X - Relevance reason
ID Y - Relevance reason

Only include notes that are actually relevant to the query."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a semantic search assistant that finds relevant information based on meaning, not just keywords."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        ai_response = response.choices[0].message.content
        
        # Parse results
        results = []
        note_dict = {note['id']: note for note in notes}
        
        for line in ai_response.split('\n'):
            match = re.search(r'ID\s+(\d+)\s*-\s*(.+)', line)
            if match:
                note_id = int(match.group(1))
                reason = match.group(2).strip()
                
                if note_id in note_dict:
                    results.append({
                        'note': note_dict[note_id],
                        'relevance': reason
                    })
        
        return results[:max_results]


class QuizGenerator:
    """Agent that generates quiz questions from notes."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance
        """
        self.pkms = pkms
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered quiz generation will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def generate_quiz(self, note_id: int, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions from a note.
        
        Args:
            note_id: ID of the note
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries
        """
        note = self.pkms.get_note(note_id)
        if not note:
            return []
        
        content = note.get('content', '')
        if not content:
            return []
        
        try:
            return self._generate_quiz_with_ai(note, num_questions)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _generate_quiz_with_ai(self, note: Dict, num_questions: int) -> List[Dict]:
        """Generate quiz questions using AI.
        
        Args:
            note: Note dictionary
            num_questions: Number of questions
            
        Returns:
            List of question dictionaries
        """
        title = note['title']
        content = note.get('content', '')
        
        prompt = f"""Generate {num_questions} quiz questions to test understanding of this study note.
Include a mix of question types: multiple choice, true/false, and short answer.

Note Title: {title}
Content:
{content}

Format each question like this:
Q1: [Question text]
Type: [multiple_choice/true_false/short_answer]
Answer: [Correct answer]
Options: [For multiple choice: A) ... B) ... C) ... D) ...]

Make questions test understanding, not just memorization."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful tutor that creates effective quiz questions to test student understanding."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000  # Increased to handle more questions (20+ questions need ~1500-2000 tokens)
        )
        
        ai_response = response.choices[0].message.content
        
        # Parse questions
        questions = []
        current_q = {}
        
        for line in ai_response.split('\n'):
            line = line.strip()
            if line.startswith('Q') and ':' in line:
                if current_q:
                    questions.append(current_q)
                current_q = {'question': line.split(':', 1)[1].strip()}
            elif line.startswith('Type:'):
                current_q['type'] = line.split(':', 1)[1].strip()
            elif line.startswith('Answer:'):
                current_q['answer'] = line.split(':', 1)[1].strip()
            elif line.startswith('Options:'):
                current_q['options'] = line.split(':', 1)[1].strip()
        
        if current_q:
            questions.append(current_q)
        
        return questions


class KnowledgeAssistant:
    """Agent that answers questions about notes and tasks using RAG."""
    
    def __init__(self, pkms: PKMS, task_manager: TaskManager):
        """Initialize with PKMS and TaskManager.
        
        Args:
            pkms: PKMS instance
            task_manager: TaskManager instance
        """
        self.pkms = pkms
        self.task_manager = task_manager
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered knowledge assistant will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def ask(self, question: str) -> str:
        """Answer a question using knowledge from notes and tasks.
        
        Args:
            question: User's question
            
        Returns:
            AI-generated answer
        """
        try:
            return self._answer_with_ai(question)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _answer_with_ai(self, question: str) -> str:
        """Use AI with RAG to answer question.
        
        Args:
            question: User's question
            
        Returns:
            AI answer based on available knowledge
        """
        # Gather context from notes and tasks
        notes = self.pkms.list_notes()
        tasks = self.task_manager.list_tasks()
        
        # Prepare context (limit to avoid token limits)
        notes_context = []
        for note in notes[:10]:
            ctx = f"\n- {note['title']}"
            if note.get('tags'):
                ctx += f" [Tags: {', '.join(note['tags'])}]"
            if note.get('content'):
                ctx += f"\n  {note['content'][:300]}..."
            notes_context.append(ctx)
        
        tasks_context = []
        for task in tasks[:10]:
            ctx = f"\n- {task['title']} (Status: {task['status']}, Priority: {task.get('priority', 'N/A')})"
            if task.get('due_date'):
                ctx += f", Due: {task['due_date']}"
            if task.get('description'):
                ctx += f"\n  {task['description'][:200]}..."
            tasks_context.append(ctx)
        
        prompt = f"""Answer this question based on the user's notes and tasks.

QUESTION: {question}

AVAILABLE NOTES:
{''.join(notes_context) if notes_context else 'No notes available'}

TASKS:
{''.join(tasks_context) if tasks_context else 'No tasks available'}

Provide a helpful, accurate answer based on the available information. If the information isn't sufficient, say so."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant that answers questions based on the user's notes and tasks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()


class NoteExpander:
    """Agent that helps expand and improve note content."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance
        """
        self.pkms = pkms
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\nWARNING: OPENAI_API_KEY not found in environment.")
            print("AI-powered note expansion will not work.")
            print("See OPENAI_SETUP.md for instructions.")
            sys.exit(1)
        
        try:
            self.openai_client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"\nERROR: Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def expand_note(self, note_id: int, instruction: str = "expand") -> str:
        """Expand or improve a note based on instruction.
        
        Args:
            note_id: ID of the note
            instruction: What to do (expand, clarify, add examples, etc.)
            
        Returns:
            Improved note content
        """
        note = self.pkms.get_note(note_id)
        if not note:
            return "Note not found."
        
        content = note.get('content', '')
        if not content:
            return "Note has no content to expand."
        
        try:
            return self._expand_with_ai(note, instruction)
        except Exception as e:
            print(f"\nERROR: OpenAI API call failed: {e}")
            print("Please check your API key and internet connection.")
            raise
    
    def _expand_with_ai(self, note: Dict, instruction: str) -> str:
        """Use AI to expand/improve note content.
        
        Args:
            note: Note dictionary
            instruction: Improvement instruction
            
        Returns:
            Improved content
        """
        title = note['title']
        content = note.get('content', '')
        tags = ', '.join(note.get('tags', []))
        
        instruction_map = {
            'expand': 'Expand this note with more detail and explanation',
            'clarify': 'Clarify and improve the explanation in this note',
            'examples': 'Add practical examples to this note',
            'simplify': 'Simplify and make this note easier to understand'
        }
        
        prompt_instruction = instruction_map.get(instruction, instruction)
        
        prompt = f"""{prompt_instruction}:

Title: {title}
Tags: {tags if tags else 'None'}

Current Content:
{content}

Provide improved content that maintains the original meaning while being more helpful for studying."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant that improves study notes while maintaining accuracy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        return response.choices[0].message.content.strip()
