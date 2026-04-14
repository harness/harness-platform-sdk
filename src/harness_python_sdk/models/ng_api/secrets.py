"""
Secret resource models for Harness SDK.

Defines request/response models for secret CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class SecretResponse(HarnessModel):
    """Secret resource response model.

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
    spec: dict
    draft: bool | None = None
    governance_metadata: dict | None = Field(None, alias="governanceMetadata")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updatedAt")


class SecretCreateRequest(HarnessModel):
    """Secret creation request model."""

    identifier: str
    name: str
    type: str
    spec: dict
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
