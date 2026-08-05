"""
WorkspaceDefaultPipeline resource models for Harness SDK.

Defines request/response models for workspacedefaultpipelines CRUD operations.
"""

from __future__ import annotations

from enum import Enum

from pydantic import AliasChoices, ConfigDict, Field

from harness_python_sdk.base_model import HarnessModel


class WorkspaceDefaultPipelineOperation(str, Enum):
    plan = "plan"
    apply = "apply"
    destroy = "destroy"
    drift = "drift"
    synth = "synth"
    diff = "diff"
    deploy = "deploy"


class WorkspaceDefaultPipelineProvisioner(str, Enum):
    terraform = "terraform"
    opentofu = "opentofu"
    terragrunt = "terragrunt"
    awscdk = "awscdk"


class WorkspaceDefaultPipelineResponse(HarnessModel):
    """WorkspaceDefaultPipeline resource response model.

    Used for both get() and list() item responses.
    """

    model_config = ConfigDict(use_enum_values=True)

    account_identifier: str = Field(
        default=None, alias=AliasChoices("account", "accountIdentifier")
    )
    org_identifier: str = Field(default=None, alias=AliasChoices("org", "orgIdentifier"))
    project_identifier: str = Field(
        default=None, alias=AliasChoices("project", "projectIdentifier")
    )
    pipeline_identifier: str = Field(
        default=None, alias=AliasChoices("pipeline", "pipelineIdentifier")
    )
    workspace_identifier: str = Field(
        default=None, alias=AliasChoices("workspace", "workspaceIdentifier")
    )
    # description: str | None = None
    # tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    operation: WorkspaceDefaultPipelineOperation
    # created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updated")


class WorkspaceDefaultPipelineCreateRequest(HarnessModel):
    """WorkspaceDefaultPipeline creation request model."""

    account_identifier: str = Field(
        default=None, alias=AliasChoices("account", "accountIdentifier")
    )
    org_identifier: str = Field(default=None, alias=AliasChoices("org", "orgIdentifier"))
    project_identifier: str = Field(
        default=None, alias=AliasChoices("project", "projectIdentifier")
    )
    pipeline_identifier: str = Field(
        default=None, alias=AliasChoices("pipeline", "pipelineIdentifier")
    )
    workspace_identifier: str = Field(
        default=None, alias=AliasChoices("workspace", "workspaceIdentifier")
    )
    #####
    # Additional Response properties
    #####
    provisioner: WorkspaceDefaultPipelineProvisioner
    operation: WorkspaceDefaultPipelineOperation
