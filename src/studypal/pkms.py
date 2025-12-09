"""PKMS (Personal Knowledge Management System) module for StudyPal."""

from typing import List, Dict, Optional
from .storage import Storage
from .utils import parse_tags


class PKMS:
    """Personal Knowledge Management System for handling notes."""
    
    def __init__(self, storage: Storage):
        """Initialize PKMS with a storage backend.
        
        Args:
            storage: Storage instance for data persistence
        """
        self.storage = storage
    
    def add_note(self, title: str, content: str = "", tags: List[str] = None) -> int:
        """Create a new note.
        
        Args:
            title: Title of the note
            content: Content of the note (Markdown format)
            tags: List of tags for categorization
            
        Returns:
            ID of the newly created note
        """
        if tags is None:
            tags = []
        
        note = {
            "title": title,
            "content": content,
            "tags": tags
        }
        return self.storage.add_note(note)
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Retrieve a note by ID.
        
        Args:
            note_id: ID of the note
            
        Returns:
            Note dictionary if found, None otherwise
        """
        return self.storage.get_note(note_id)
    
    def list_notes(self, tag: Optional[str] = None) -> List[Dict]:
        """List all notes, optionally filtered by tag.
        
        Args:
            tag: Optional tag to filter by
            
        Returns:
            List of note dictionaries
        """
        data = self.storage.load_notes()
        notes = data['notes']
        
        if tag:
            notes = [n for n in notes if tag in n.get('tags', [])]
        
        return notes
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by keyword in title or content.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching note dictionaries
        """
        query_lower = query.lower()
        data = self.storage.load_notes()
        results = []
        
        for note in data['notes']:
            title_match = query_lower in note['title'].lower()
            content_match = query_lower in note.get('content', '').lower()
            tags_match = any(query_lower in tag.lower() for tag in note.get('tags', []))
            
            if title_match or content_match or tags_match:
                results.append(note)
        
        return results
    
    def update_note(self, note_id: int, title: Optional[str] = None, 
                    content: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
        """Update an existing note.
        
        Args:
            note_id: ID of the note to update
            title: New title (optional)
            content: New content (optional)
            tags: New tags list (optional)
            
        Returns:
            True if note was updated, False if not found
        """
        updates = {}
        if title is not None:
            updates['title'] = title
        if content is not None:
            updates['content'] = content
        if tags is not None:
            updates['tags'] = tags
        
        return self.storage.update_note(note_id, updates)
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note.
        
        Args:
            note_id: ID of the note to delete
            
        Returns:
            True if note was deleted, False if not found
        """
        return self.storage.delete_note(note_id)
    
    def link_notes(self, from_id: int, to_id: int, link_type: str = "related") -> bool:
        """Create a link between two notes.
        
        Args:
            from_id: ID of the source note
            to_id: ID of the target note
            link_type: Type of link relationship
            
        Returns:
            True if link was created, False if notes don't exist
        """
        # Verify both notes exist
        if not self.storage.get_note(from_id) or not self.storage.get_note(to_id):
            return False
        
        self.storage.add_link(from_id, to_id, link_type)
        return True
    
    def get_linked_notes(self, note_id: int) -> List[Dict]:
        """Get all notes linked to a given note.
        
        Args:
            note_id: ID of the note
            
        Returns:
            List of linked note dictionaries with link information
        """
        links = self.storage.get_links(note_id)
        linked_notes = []
        
        for link in links:
            # Determine which note is the other one
            other_id = link['to_note_id'] if link['from_note_id'] == note_id else link['from_note_id']
            other_note = self.storage.get_note(other_id)
            
            if other_note:
                linked_note = other_note.copy()
                linked_note['link_type'] = link['link_type']
                linked_note['link_direction'] = 'outgoing' if link['from_note_id'] == note_id else 'incoming'
                linked_notes.append(linked_note)
        
        return linked_notes
    
    def get_all_tags(self) -> List[str]:
        """Get a list of all unique tags used in notes.
        
        Returns:
            List of unique tag strings
        """
        data = self.storage.load_notes()
        tags = set()
        
        for note in data['notes']:
            tags.update(note.get('tags', []))
        
        return sorted(list(tags))
    
    def add_tags(self, note_id: int, new_tags: List[str]) -> bool:
        """Add tags to an existing note.
        
        Args:
            note_id: ID of the note
            new_tags: List of tags to add
            
        Returns:
            True if tags were added, False if note not found
        """
        note = self.storage.get_note(note_id)
        if not note:
            return False
        
        current_tags = set(note.get('tags', []))
        current_tags.update(new_tags)
        
        return self.storage.update_note(note_id, {'tags': list(current_tags)})
    
    def remove_tags(self, note_id: int, tags_to_remove: List[str]) -> bool:
        """Remove tags from an existing note.
        
        Args:
            note_id: ID of the note
            tags_to_remove: List of tags to remove
            
        Returns:
            True if tags were removed, False if note not found
        """
        note = self.storage.get_note(note_id)
        if not note:
            return False
        
        current_tags = set(note.get('tags', []))
        current_tags.difference_update(tags_to_remove)
        
        return self.storage.update_note(note_id, {'tags': list(current_tags)})
