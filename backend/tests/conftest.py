"""Pytest configuration for tests."""

import pytest

# Configure pytest-asyncio
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as an asyncio test"
    )
