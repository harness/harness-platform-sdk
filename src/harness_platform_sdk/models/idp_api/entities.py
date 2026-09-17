"""Entity resource models for Harness SDK.

Defines request/response models for entities CRUD operations.
"""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from harness_platform_sdk.base_model import HarnessModel


class EntityResponse(HarnessModel):
    """Entity resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: Optional[str] = Field(default=None, alias="orgIdentifier")
    project_identifier: Optional[str] = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: list[str, str] | None = []
    #####
    # Additional Response properties
    #####
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updatedAt")


class EntityCreateRequest(HarnessModel):
    """Entity creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: list[str, str] | None = []
    type: str
    owner: str


class EntityWorkflowCreateRequest(EntityCreateRequest):
    """Workflow Specific Spec."""

    kind: str = Field(default="workflow", frozen=True)
    parameters: list[dict, dict]
    steps: list[dict, dict]
    links: list[dict, dict]
    outputs: list[dict, dict]


class EntityComponentCreateRequest(EntityCreateRequest):
    """Component Specific Spec."""

    kind: str = Field(default="component", frozen=True)
    lifecycle: str
    metadata: dict | None = {}


class EntityResourceCreateRequest(EntityCreateRequest):
    """Resource Specific Spec."""

    kind: str = Field(default="resource", frozen=True)
    lifecycle: str
    metadata: dict | None = {}


class EntitySystemCreateRequest(EntityCreateRequest):
    """System Specific Spec."""

    kind: str = Field(default="system", frozen=True)
    lifecycle: str
    metadata: dict | None = {}
