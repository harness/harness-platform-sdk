"""Resource Group resource models for Harness SDK.

Defines request/response models for resource group CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_platform_sdk.base_model import HarnessModel


class ResourceGroupResponse(HarnessModel):
    """Resource Group resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    color: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = {}
    allowed_scope_levels: list[str] = Field(..., alias="allowedScopeLevels")
    resource_filter: dict | None = Field(None, alias="resourceFilter")
    included_scopes: list[dict] = Field(..., alias="includedScopes")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastModifiedAt")


class ResourceGroupCreateRequest(HarnessModel):
    """Resource Group creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    color: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = {}
    allowed_scope_levels: list[str] = Field(..., alias="allowedScopeLevels")
    resource_filter: dict | None = Field(None, alias="resourceFilter")
    included_scopes: list[dict] = Field(..., alias="includedScopes")
