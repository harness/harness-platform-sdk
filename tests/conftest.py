"""
Pytest configuration and fixtures for all test suites.
"""

import pytest


@pytest.fixture
def anyio_backend():
    """Use threaded backend for async tests."""
    return "asyncio"
