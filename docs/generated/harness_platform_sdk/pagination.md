Module harness_platform_sdk.pagination
======================================
Pagination support for Harness SDK.

Defines pagination styles (OFFSET/CURSOR) and the interface for paginated requests.
Implementation lives on HarnessClient._paginate().

Classes
-------

`PaginationStyle(*values)`
:   Pagination style enum for API endpoints.
    
    Attributes:
        OFFSET: Offset-based pagination (using pageIndex/pageSize or skip/limit).
        CURSOR: Cursor-based pagination (using pageToken/nextPageToken).

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `CURSOR`
    :   The type of the None singleton.

    `OFFSET`
    :   The type of the None singleton.