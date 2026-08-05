"""
WorkspaceVariable resource models for Harness SDK.

Defines request/response models for workspacevariables CRUD operations.
"""

from __future__ import annotations

from enum import Enum

from pydantic import AliasChoices, ConfigDict, Field

from harness_python_sdk.base_model import HarnessModel


class WorkspaceVariableKind(str, Enum):
    env = "env"
    tf = "tf"


class WorkspaceValueType(str, Enum):
    string = "string"
    secret = "secret"


class WorkspaceVariableResponse(HarnessModel):
    """WorkspaceVariable resource response model.

    Used for both get() and list() item responses.
    """

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
    workspace_identifier: str = Field(alias=AliasChoices("workspace", "workspaceIdentifier"))
    #####
    # Additional Response properties
    #####
    identifier: str = Field(alias=AliasChoices("key", "identifier"))
    kind: WorkspaceVariableKind
    value: str
    value_type: WorkspaceValueType
    created_at: int = Field(default=None, alias="created")
    updated_at: int = Field(default=None, alias="updated")


class WorkspaceVariableCreateRequest(HarnessModel):
    """WorkspaceVariable creation request model."""

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
    workspace_identifier: str
    #####
    # Additional Response properties
    #####
    identifier: str = Field(alias=AliasChoices("key", "identifier"))
    kind: WorkspaceVariableKind
    value: str
    value_type: WorkspaceValueType
