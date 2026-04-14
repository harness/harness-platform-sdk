"""
EnvironmentV2 resource models for Harness SDK.

Defines request/response models for environment CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class EnvironmentV2Response(HarnessModel):
    """EnvironmentV2 resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    type: str
    store_type: str = Field(default=None, alias="storeType")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updatedAt")


class EnvironmentV2CreateRequest(HarnessModel):
    """EnvironmentV2 creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    type: str
    store_type: str = Field(default=None, alias="storeType")
