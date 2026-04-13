"""
Role Assignment resource models for Harness SDK.

Defines request/response models for role assignment CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class RoleAssignmentResponse(HarnessModel):
    """Role Assignment resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    role_identifier: str = Field(..., alias="roleIdentifier")
    scope: dict
    principal: dict
    disabled: bool | None = None
    created: int | None = None
    updated: int | None = None


class RoleAssignmentCreateRequest(HarnessModel):
    """Role Assignment creation request model."""

    role_identifier: str = Field(..., alias="roleIdentifier")
    scope: dict
    principal: dict
    disabled: bool | None = None


class RoleAssignmentUpdateRequest(HarnessModel):
    """Role Assignment update request model.

    Note: Updates via PUT are not available per spec.
    This model exists for API consistency but updates should use delete + create pattern.
    """

    role_identifier: str = Field(..., alias="roleIdentifier")
    scope: dict
    principal: dict
    disabled: bool | None = None
