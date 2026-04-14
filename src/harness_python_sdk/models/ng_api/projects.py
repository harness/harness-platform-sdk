"""
Project resource models for Harness SDK.

Defines request/response models for project CRUD operations.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from harness_python_sdk.base_model import HarnessModel


class ProjectResponse(HarnessModel):
    """Project resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(..., alias="orgIdentifier")
    color: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastModifiedAt")
    last_moved_at: int = Field(default=None, alias="lastMovedAt")

    @field_validator("last_moved_at", mode="before")
    @classmethod
    def allow_null_string(cls, v):
        if v == "null" or v is None:
            return 0
        return v


class ProjectCreateRequest(HarnessModel):
    """Project creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    color: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None
