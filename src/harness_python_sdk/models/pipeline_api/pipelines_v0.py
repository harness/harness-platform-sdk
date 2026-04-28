"""
Pipeline resource models for Harness SDK.

Defines request/response models for pipeline CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class PipelineV0Response(HarnessModel):
    """Pipeline resource response model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    stages: list[dict]
    # variables: list[dict]
    created_at: int = Field(default=0, alias="createdAt")
    updated_at: int = Field(default=0, alias="lastUpdatedAt")


class PipelineV0ListResponse(HarnessModel):
    """Pipeline resource response list model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    modules: list[str]
    version: int
    yaml_version: int = Field(default=0, alias="yamlVersion")
    store_type: str = Field(default=None, alias="storeType")
    num_of_stages: int = Field(default=None, alias="numOfStages")
    stage_names: list[str] = Field(default=[], alias="stageNames")
    execution_summary_info: dict = Field(default={}, alias="executionSummaryInfo")
    recent_executions_info: list[dict] = Field(default=[], alias="recentExecutionsInfo")
    git_details: dict[str, dict] = Field(default={}, alias="gitDetails")
    entity_validity_details: dict = Field(default={}, alias="entityValidityDetails")
    is_draft: bool = Field(default=False, alias="isDraft")
    is_inline_hc_entity: bool = Field(default=False, alias="isInlineHCEntity")
    enable_dag: bool = Field(default=False, alias="enableDAG")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastUpdatedAt")


class PipelineV0CreateRequest(HarnessModel):
    """Pipeline creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    stages: list[dict]
    variables: list[dict] | None = []
