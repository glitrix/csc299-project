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
    """Agent that suggests links between notes based on content analysis."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance to analyze notes
        """
        self.pkms = pkms
    
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
        """Suggest notes that might be related to the given note.
        
        Args:
            note_id: ID of the note to find links for
            min_similarity: Minimum similarity threshold
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of suggested notes with similarity scores
        """
        target_note = self.pkms.get_note(note_id)
        if not target_note:
            return []
        
        all_notes = self.pkms.list_notes()
        suggestions = []
        
        # Get existing links to avoid suggesting them
        existing_links = self.pkms.get_linked_notes(note_id)
        existing_ids = {note['id'] for note in existing_links}
        
        for note in all_notes:
            # Skip the target note itself and already linked notes
            if note['id'] == note_id or note['id'] in existing_ids:
                continue
            
            similarity = self._calculate_similarity(target_note, note)
            
            if similarity >= min_similarity:
                suggestions.append({
                    'note': note,
                    'similarity': similarity
                })
        
        # Sort by similarity (highest first) and limit results
        suggestions.sort(key=lambda x: x['similarity'], reverse=True)
        return suggestions[:max_suggestions]


class TagSuggester:
    """Agent that suggests tags for notes based on content."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance to analyze notes
        """
        self.pkms = pkms
    
    def suggest_tags(self, note_id: int, max_suggestions: int = 5) -> List[str]:
        """Suggest tags for a note based on its content and existing tags.
        
        Args:
            note_id: ID of the note
            max_suggestions: Maximum number of tag suggestions
            
        Returns:
            List of suggested tag strings
        """
        note = self.pkms.get_note(note_id)
        if not note:
            return []
        
        # Get all existing tags in the system
        all_tags = self.pkms.get_all_tags()
        current_tags = set(note.get('tags', []))
        
        # Extract keywords from the note
        text = f"{note['title']} {note.get('content', '')}"
        keywords = re.findall(r'\b\w+\b', text.lower())
        keyword_counts = Counter(keywords)
        
        # Find tags that match keywords in the note
        suggestions = []
        for tag in all_tags:
            if tag in current_tags:
                continue
            
            tag_lower = tag.lower()
            # Check if tag appears in the note content
            if tag_lower in [k.lower() for k in keywords]:
                count = keyword_counts.get(tag_lower, 0)
                suggestions.append((tag, count))
        
        # Sort by frequency and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in suggestions[:max_suggestions]]


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
    """Agent that generates summaries of notes."""
    
    def __init__(self, pkms: PKMS):
        """Initialize with PKMS instance.
        
        Args:
            pkms: PKMS instance
        """
        self.pkms = pkms
    
    def generate_summary(self, note_id: int, max_sentences: int = 3) -> str:
        """Generate a summary of a note.
        
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
        
        # Simple extractive summarization
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return content
        
        # Extract key sentences (simple approach: first, middle, last)
        if len(sentences) >= 3:
            indices = [0, len(sentences) // 2, -1]
        elif len(sentences) == 2:
            indices = [0, -1]
        else:
            indices = [0]
        
        summary_sentences = [sentences[i] for i in indices[:max_sentences]]
        return '. '.join(summary_sentences) + '.'
    
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
