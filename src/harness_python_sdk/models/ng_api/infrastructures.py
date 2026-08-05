"""
Infrastructure resource models for Harness SDK.

Defines request/response models for infrastructure CRUD operations.
"""

from __future__ import annotations

from pydantic import AliasChoices, Field

from harness_python_sdk.base_model import HarnessModel


class InfrastructureResponse(HarnessModel):
    """Infrastructure resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(
        default=None, alias=AliasChoices("accountIdentifier", "accountId")
    )
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    environment_identifier: str = Field(
        ..., alias=AliasChoices("environmentIdentifier", "environmentRef")
    )
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    type: str
    deployment_type: str
    spec: dict
    allow_simultaneous_deployments: bool = Field(
        default=False, alias="allowSimultaneousDeployments"
    )
    # created_at: int = Field(default=None, alias="createdAt")
    # updated_at: int = Field(default=None, alias="updatedAt")


class InfrastructureCreateRequest(HarnessModel):
    """Infrastructure creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    environment_identifier: str = Field(..., alias="environmentIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    type: str
    deployment_type: str
    spec: dict
    allow_simultaneous_deployments: bool = Field(
        default=False, alias="allowSimultaneousDeployments"
    )
