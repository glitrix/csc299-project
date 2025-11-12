"""Utility functions for StudyPal."""

from typing import List
from datetime import datetime


def parse_tags(tags_str: str) -> List[str]:
    """Parse comma-separated tags string into a list.
    
    Args:
        tags_str: Comma-separated string of tags
        
    Returns:
        List of tag strings
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]


def format_date(date_str: str) -> str:
    """Format ISO date string to readable format.
    
    Args:
        date_str: ISO format date string
        
    Returns:
        Formatted date string
    """
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return date_str


def validate_priority(priority: int) -> bool:
    """Check if priority value is valid (1-5).
    
    Args:
        priority: Priority value to validate
        
    Returns:
        True if valid, False otherwise
    """
    return 1 <= priority <= 5


def validate_status(status: str) -> bool:
    """Check if status is valid.
    
    Args:
        status: Status string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_statuses = ["todo", "in_progress", "done"]
    return status in valid_statuses


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
