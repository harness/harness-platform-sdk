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
    org: str | None = None
    project: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None
    created: int | None = None
    updated: int | None = None
    spec: dict | None = None
    draft: bool | None = None
    governance_metadata: dict | None = Field(None, alias="governanceMetadata")


class SecretCreateRequest(HarnessModel):
    """Secret creation request model."""

    identifier: str
    name: str
    spec: dict
    org: str | None = None
    project: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None


class SecretUpdateRequest(HarnessModel):
    """Secret update request model."""

    identifier: str
    name: str
    spec: dict
    description: str | None = None
    tags: dict[str, str] | None = None
