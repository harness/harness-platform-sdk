"""
Role resource models for Harness SDK.

Defines request/response models for role CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class RoleResponse(HarnessModel):
    """Role resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    allowed_scope_levels: list[str] = Field(..., alias="allowedScopeLevels")
    permissions: list[str] | None = None
    description: str | None = None
    tags: dict[str, str] | None = {}
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastModifiedAt")


class RoleCreateRequest(HarnessModel):
    """Role creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    allowed_scope_levels: list[str] = Field(..., alias="allowedScopeLevels")
    description: str | None = None
    permissions: list[str] | None = None
    tags: dict[str, str] | None = {}
