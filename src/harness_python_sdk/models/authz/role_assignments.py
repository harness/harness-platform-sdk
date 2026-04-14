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
    resource_group_identifier: str = Field(..., alias="resourceGroupIdentifier")
    role_reference: dict = Field(..., alias="roleReference")
    principal: dict
    disabled: bool | None = False
    created: int | None = None
    updated: int | None = None


class RoleAssignmentCreateRequest(HarnessModel):
    """Role Assignment creation request model."""

    identifier: str | None = None
    role_identifier: str = Field(..., alias="roleIdentifier")
    resource_group_identifier: str = Field(..., alias="resourceGroupIdentifier")
    role_reference: dict = Field(..., alias="roleReference")
    principal: dict
    disabled: bool | None = False
