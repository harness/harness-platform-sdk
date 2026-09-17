"""Service resource models for Harness SDK.

Defines request/response models for service CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_platform_sdk.base_model import HarnessModel


class ServiceResponse(HarnessModel):
    """Service resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    type: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    manifests: list[dict] | None = []
    artifacts: dict | None = {}
    store_type: str = Field(default="INLINE", alias="storeType")
    is_v2_service: bool = Field(default=False, alias="v2Service")
    created_at: int = Field(default=0, alias="createdAt")
    updated_at: int = Field(default=0, alias="updatedAt")


class ServiceCreateRequest(HarnessModel):
    """Service creation request model."""

    identifier: str
    name: str
    type: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    manifests: list[dict] | None = []
    artifacts: dict | None = {}
    store_type: str = Field(default=None, alias="storeType")
    is_v2_service: bool = Field(default=False, alias="v2Service")
