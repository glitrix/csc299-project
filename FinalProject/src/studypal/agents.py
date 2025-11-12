"""AI Agents module for StudyPal - provides intelligent assistance."""

import os
from typing import List, Dict, Optional
from collections import Counter
import re
from datetime import datetime, timedelta
from .storage import Storage
from .pkms import PKMS
from .tasks import TaskManager


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
    
    def plan_week(self) -> Dict[str, List[Dict]]:
        """Create a weekly study plan based on tasks and deadlines.
        
        Returns:
            Dictionary mapping day names to lists of planned activities
        """
        # Get all incomplete tasks
        todo_tasks = self.task_manager.list_tasks(status="todo")
        in_progress = self.task_manager.list_tasks(status="in_progress")
        all_tasks = todo_tasks + in_progress
        
        # Sort by priority (highest first) and due date
        def task_sort_key(task):
            due_date = task.get('due_date', '9999-12-31')
            priority = task.get('priority', 1)
            return (due_date, -priority)
        
        all_tasks.sort(key=task_sort_key)
        
        # Create 7-day plan
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        plan = {day: [] for day in days}
        
        # Distribute tasks across the week
        # Priority 5 and 4 tasks get more time
        task_index = 0
        for day_index, day in enumerate(days):
            # Add 2-3 tasks per day, prioritizing high priority tasks
            tasks_for_day = 0
            max_tasks = 3 if day_index < 5 else 2  # More tasks on weekdays
            
            while task_index < len(all_tasks) and tasks_for_day < max_tasks:
                task = all_tasks[task_index]
                
                # Estimate time based on priority
                priority = task.get('priority', 2)
                estimated_hours = 3 if priority >= 4 else 2 if priority >= 3 else 1
                
                plan[day].append({
                    'task': task,
                    'estimated_hours': estimated_hours,
                    'type': 'task'
                })
                
                tasks_for_day += 1
                task_index += 1
        
        # Add review time for notes (on days with lighter task load)
        notes = self.pkms.list_notes()
        if notes:
            for day in days:
                if len(plan[day]) < 2:  # Days with fewer tasks
                    # Suggest reviewing a note
                    note_index = days.index(day) % len(notes)
                    plan[day].append({
                        'note': notes[note_index],
                        'estimated_hours': 0.5,
                        'type': 'review'
                    })
        
        return plan
    
    def suggest_daily_schedule(self) -> List[Dict]:
        """Suggest tasks for today based on due dates and priorities.
        
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
        
        # Sort by priority and due date
        # Use empty string for None due_date to handle comparison properly
        daily_tasks.sort(key=lambda t: (t.get('due_date') or '9999-12-31', -t.get('priority', 1)))
        
        return daily_tasks[:5]  # Return top 5 tasks


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
