"""
Pagination support for Harness SDK.

Defines pagination styles (OFFSET/CURSOR) and the interface for paginated requests.
Implementation lives on HarnessClient._paginate().
"""

from enum import Enum


class PaginationStyle(str, Enum):
    """Pagination style enum for API endpoints.

    Attributes:
        OFFSET: Offset-based pagination (using pageIndex/pageSize or skip/limit).
        CURSOR: Cursor-based pagination (using pageToken/nextPageToken).
    """

    OFFSET = "offset"
    CURSOR = "cursor"
