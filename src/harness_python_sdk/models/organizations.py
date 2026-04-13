"""
Organization resource models for Harness SDK.

Defines request/response models for organization CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class OrganizationResponse(HarnessModel):
    """Organization resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    description: str | None = None
    tags: dict[str, str] | None = None
    harness_managed: bool | None = Field(None, alias="harnessManaged")
    created: int | None = Field(None, alias="createdAt")
    updated: int | None = Field(None, alias="lastModifiedAt")


class OrganizationCreateRequest(HarnessModel):
    """Organization creation request model."""

    identifier: str
    name: str
    description: str | None = None
    tags: dict[str, str] | None = None


class OrganizationUpdateRequest(HarnessModel):
    """Organization update request model."""

    identifier: str
    name: str
    description: str | None = None
    tags: dict[str, str] | None = None

    def to_dict(self):
        return {"organization": self.dict()}
