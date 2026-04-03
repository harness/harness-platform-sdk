"""
Pagination support for Harness SDK.

Defines pagination styles (OFFSET/CURSOR) and the interface for paginated requests.
Implementation lives on HarnessClient._paginate().
"""

from enum import Enum


class PaginationStyle(str, Enum):
    """Pagination style enum for API endpoints."""

    OFFSET = "offset"
    CURSOR = "cursor"
