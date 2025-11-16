"""Pytest configuration for StudyPal tests."""

import os
import pytest

# Set a dummy OpenAI API key for tests that need it
# This allows tests to run without requiring an actual API key
@pytest.fixture(autouse=True)
def mock_openai_api_key(monkeypatch):
    """Set a mock OpenAI API key for all tests."""
    if not os.getenv("OPENAI_API_KEY"):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy-key-for-testing")

@pytest.fixture
def skip_if_no_valid_api_key():
    """Skip test if no valid OpenAI API key is configured."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key.startswith("sk-test"):
        pytest.skip("Test requires a valid OpenAI API key")
