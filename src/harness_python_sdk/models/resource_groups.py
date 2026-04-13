"""
Resource Group resource models for Harness SDK.

Defines request/response models for resource group CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class ResourceGroupResponse(HarnessModel):
    """Resource Group resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    description: str | None = None
    resource_filter: dict | None = Field(None, alias="resourceFilter")
    created: int | None = None
    updated: int | None = None


class ResourceGroupCreateRequest(HarnessModel):
    """Resource Group creation request model."""

    identifier: str
    name: str
    resource_filter: dict | None = Field(None, alias="resourceFilter")
    description: str | None = None


class ResourceGroupUpdateRequest(HarnessModel):
    """Resource Group update request model."""

    identifier: str
    name: str
    resource_filter: dict | None = Field(None, alias="resourceFilter")
    description: str | None = None
