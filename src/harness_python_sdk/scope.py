"""
Scope management for Harness SDK.

Scope is a frozen model representing the account/organization/project context
for API calls. Scopes are resolved once at the start of each request.
"""

from pydantic import BaseModel, ConfigDict


class Scope(BaseModel):
    """Represents the account/org/project scope for API requests.

    The scope is frozen — once created, it cannot be modified.
    The account_id is required; org and project are optional.

    Attributes:
        account_id: Harness account identifier (required).
        org: Harness organization identifier (optional).
        project: Harness project identifier (optional).
    """

    account_id: str
    org: str | None = None
    project: str | None = None

    model_config = ConfigDict(frozen=True)
