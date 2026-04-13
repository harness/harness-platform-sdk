"""
Project resource models for Harness SDK.

Defines request/response models for project CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class ProjectResponse(HarnessModel):
    """Project resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    org: str
    description: str | None = None
    tags: dict[str, str] | None = None
    is_favorite: bool = Field(False, alias="isFavorite")
    created: int | None = None
    updated: int | None = None


class ProjectCreateRequest(HarnessModel):
    """Project creation request model."""

    identifier: str
    name: str
    description: str | None = None
    tags: dict[str, str] | None = None


class ProjectUpdateRequest(HarnessModel):
    """Project update request model."""

    identifier: str
    name: str
    description: str | None = None
    tags: dict[str, str] | None = None
