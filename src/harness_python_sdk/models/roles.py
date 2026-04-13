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
    allowed_scope_levels: list[str] = Field(..., alias="allowedScopeLevels")
    description: str | None = None
    permissions: list[str] | None = None
    created: int | None = None
    updated: int | None = None


class RoleCreateRequest(HarnessModel):
    """Role creation request model."""

    identifier: str
    name: str
    allowed_scope_levels: list[str] = Field(..., alias="allowedScopeLevels")
    description: str | None = None
    permissions: list[str] | None = None


class RoleUpdateRequest(HarnessModel):
    """Role update request model."""

    identifier: str
    name: str
    description: str | None = None
    permissions: list[str] | None = None
