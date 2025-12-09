"""Tests for PKMS functionality."""

import pytest
import tempfile
import shutil
from pathlib import Path
from src.studypal.storage import Storage
from src.studypal.pkms import PKMS


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    temp_dir = tempfile.mkdtemp()
    storage = Storage(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


@pytest.fixture
def pkms(temp_storage):
    """Create a PKMS instance for testing."""
    return PKMS(temp_storage)


def test_add_note(pkms):
    """Test adding a new note."""
    note_id = pkms.add_note("Test Note", "Test content", ["test", "sample"])
    assert note_id == 1
    
    note = pkms.get_note(note_id)
    assert note is not None
    assert note['title'] == "Test Note"
    assert note['content'] == "Test content"
    assert "test" in note['tags']
    assert "sample" in note['tags']


def test_get_note(pkms):
    """Test retrieving a note."""
    note_id = pkms.add_note("Test Note")
    note = pkms.get_note(note_id)
    
    assert note is not None
    assert note['id'] == note_id
    assert note['title'] == "Test Note"


def test_get_nonexistent_note(pkms):
    """Test retrieving a non-existent note."""
    note = pkms.get_note(999)
    assert note is None


def test_list_notes(pkms):
    """Test listing all notes."""
    pkms.add_note("Note 1")
    pkms.add_note("Note 2")
    pkms.add_note("Note 3")
    
    notes = pkms.list_notes()
    assert len(notes) == 3


def test_list_notes_by_tag(pkms):
    """Test listing notes filtered by tag."""
    pkms.add_note("Note 1", tags=["python"])
    pkms.add_note("Note 2", tags=["java"])
    pkms.add_note("Note 3", tags=["python", "programming"])
    
    python_notes = pkms.list_notes(tag="python")
    assert len(python_notes) == 2


def test_search_notes(pkms):
    """Test searching notes."""
    pkms.add_note("Python Basics", "Learn Python programming")
    pkms.add_note("Java Fundamentals", "Learn Java")
    pkms.add_note("Python Advanced", "Advanced Python concepts")
    
    results = pkms.search_notes("python")
    assert len(results) == 2


def test_update_note(pkms):
    """Test updating a note."""
    note_id = pkms.add_note("Original Title", "Original content")
    
    success = pkms.update_note(note_id, title="Updated Title", content="Updated content")
    assert success
    
    note = pkms.get_note(note_id)
    assert note['title'] == "Updated Title"
    assert note['content'] == "Updated content"


def test_delete_note(pkms):
    """Test deleting a note."""
    note_id = pkms.add_note("Test Note")
    
    success = pkms.delete_note(note_id)
    assert success
    
    note = pkms.get_note(note_id)
    assert note is None


def test_link_notes(pkms):
    """Test linking two notes."""
    note1_id = pkms.add_note("Note 1")
    note2_id = pkms.add_note("Note 2")
    
    success = pkms.link_notes(note1_id, note2_id, "related")
    assert success
    
    linked = pkms.get_linked_notes(note1_id)
    assert len(linked) == 1
    assert linked[0]['id'] == note2_id


def test_get_all_tags(pkms):
    """Test getting all unique tags."""
    pkms.add_note("Note 1", tags=["python", "programming"])
    pkms.add_note("Note 2", tags=["java", "programming"])
    pkms.add_note("Note 3", tags=["python"])
    
    tags = pkms.get_all_tags()
    assert set(tags) == {"python", "java", "programming"}


def test_add_tags(pkms):
    """Test adding tags to an existing note."""
    note_id = pkms.add_note("Test Note", tags=["initial"])
    
    success = pkms.add_tags(note_id, ["new", "additional"])
    assert success
    
    note = pkms.get_note(note_id)
    assert set(note['tags']) == {"initial", "new", "additional"}


def test_remove_tags(pkms):
    """Test removing tags from a note."""
    note_id = pkms.add_note("Test Note", tags=["tag1", "tag2", "tag3"])
    
    success = pkms.remove_tags(note_id, ["tag2"])
    assert success
    
    note = pkms.get_note(note_id)
    assert set(note['tags']) == {"tag1", "tag3"}
