"""
Service resource models for Harness SDK.

Defines request/response models for service CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class ServiceResponse(HarnessModel):
    """Service resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    org: str
    project: str
    description: str | None = None
    tags: dict[str, str] | None = None
    service_yaml: str | None = Field(None, alias="serviceYaml")
    created: int | None = None
    updated: int | None = None


class ServiceCreateRequest(HarnessModel):
    """Service creation request model."""

    identifier: str
    name: str
    service_yaml: str | None = Field(None, alias="serviceYaml")
    description: str | None = None
    tags: dict[str, str] | None = None


class ServiceUpdateRequest(HarnessModel):
    """Service update request model."""

    identifier: str
    name: str
    service_yaml: str | None = Field(None, alias="serviceYaml")
    description: str | None = None
    tags: dict[str, str] | None = None
