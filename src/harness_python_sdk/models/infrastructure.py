"""
Infrastructure resource models for Harness SDK.

Defines request/response models for infrastructure CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class InfrastructureResponse(HarnessModel):
    """Infrastructure resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    org: str | None = None
    project: str | None = None
    account: str | None = None
    environment: str | None = None
    type: str
    description: str | None = None
    tags: dict[str, str] | None = None
    created: int | None = None
    updated: int | None = None
    harness_version: str | None = Field(None, alias="harnessVersion")
    yaml: str | None = None


class InfrastructureCreateRequest(HarnessModel):
    """Infrastructure creation request model."""

    identifier: str
    name: str
    type: str
    environment: str
    org: str | None = None
    project: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None
    yaml: str | None = None


class InfrastructureUpdateRequest(HarnessModel):
    """Infrastructure update request model."""

    identifier: str
    name: str
    type: str
    environment: str
    description: str | None = None
    tags: dict[str, str] | None = None
    yaml: str | None = None
