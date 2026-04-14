"""
Trigger resource models for Harness SDK.

Defines request/response models for trigger CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class TriggerV0Response(HarnessModel):
    """Trigger resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(..., alias="orgIdentifier")
    project_identifier: str = Field(..., alias="projectIdentifier")
    pipeline_identifier: str = Field(..., alias="pipelineIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    type: str | None = None
    enabled: bool | None = False
    source: dict | None = {}
    inputs: dict | None = {}
    webhook_url: str = Field(default=None, alias="webhookUrl")
    stages_to_execute: list[str] = Field(default=[], alias="stagesToExecute")
    encrypted_webhook_secret_identifier: str = Field(default=None, alias="encryptedWebhookSecretIdentifier")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updatedAt")

class TriggerV0ListResponse(HarnessModel):
    """Trigger resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    type: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(..., alias="orgIdentifier")
    project_identifier: str = Field(..., alias="projectIdentifier")
    pipeline_identifier: str = Field(..., alias="pipelineIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    # modules: list[str]
    # version: int
    yaml_version: int = Field(default=0, alias="yamlVersion")
    store_type: str = Field(default=None, alias="storeType")
    num_of_stages: int = Field(default=None, alias="numOfStages")
    stage_names: list[str] = Field(default=[], alias="stageNames")
    execution_summary_info: dict = Field(default={}, alias="executionSummaryInfo")
    recent_executions_info: list[str] = Field(default=[], alias="recentExecutionsInfo")
    git_details: dict[str, dict] = Field(default={}, alias="gitDetails")
    entity_validity_details: dict = Field(default={}, alias="entityValidityDetails")
    is_draft: bool = Field(default=False, alias="isDraft")
    is_inline_hc_entity: bool = Field(default=False, alias="isInlineHCEntity")
    enable_dag: bool = Field(default=False, alias="enableDAG")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastUpdatedAt")


class TriggerV0CreateRequest(HarnessModel):
    """Trigger creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    pipeline_identifier: str = Field(..., alias="pipelineIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    enabled: bool | None = False
    source: dict | None = {}
    inputs: dict | None = {}
    stages_to_execute: list[str] = Field(default=[], alias="stagesToExecute")
    encrypted_webhook_secret_identifier: str = Field(default=None, alias="encryptedWebhookSecretIdentifier")
