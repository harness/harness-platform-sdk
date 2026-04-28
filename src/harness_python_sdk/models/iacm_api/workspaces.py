"""
Workspace resource models for Harness SDK.

Defines request/response models for workspace CRUD operations.
"""

from __future__ import annotations

from pydantic import Field, AliasChoices, model_validator, field_validator

from harness_python_sdk.base_model import HarnessModel


class WorkspaceCore(HarnessModel):
    """Workspace resource cor model.

    Used as root for all models.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias=AliasChoices("accountId","accountIdentifier"))
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    created_at: int = Field(default=None, alias=AliasChoices("createdAt","created"))
    updated_at: int = Field(default=None, alias=AliasChoices("lastUpdatedAt","updatedAt","updated"))


    default_pipelines: dict | None = {}
    cost_estimation_enabled: bool | None = False
    provider_connector: str | None = ""
    provider_connectors: list[dict] | None = []
    provisioner: str
    provisioner_configuration: dict | None = {}
    provisioner_version: str | None = "latest"
    prune_sensitive_data: bool | None = False

    repository: str | None = ""
    repository_branch: str | None = None
    repository_commit: str | None = None
    repository_connector: str | None = ""
    repository_path: str | None = ""
    repository_sha: str | None = None
    repository_submodules: str | None = "false"

    environment_variables: dict | None = {}
    terraform_variable_files: list[dict] | None = []
    terraform_variables: dict | None = {}
    variable_sets: list[str] | None = []

class WorkspaceResponse(WorkspaceCore):
    """Workspace resource response model.

    Used for both get() and list() item responses.
    """

    backend_locked: bool | None = False
    budget: float | None = 0.0
    cost_breakdown_json: dict | str | None = {}
    cost_diff_json: dict | str | None = {}
    modules_json: str | None = None
    providers_json: dict | None = {}
    status: str | None = "inactive"

    @field_validator("providers_json", mode="before")
    @classmethod
    def normalize_providers_json(cls, v):
        if v == "" or v is None:
            return {}
        return v


class WorkspaceCreateRequest(WorkspaceCore):
    """Workspace creation request model."""

    @model_validator(mode='after')
    def check_at_least_one(self) -> 'WorkspaceCreateRequest':
        # Check if both fields are null
        if self.repository_branch is None and self.repository_commit is None and self.repository_sha is None:
            raise ValueError('One of "repository_branch", "repository_commit", or "repository_sha" must be provided.')
        return self
