"""
Inputset resource models for Harness SDK.

Defines request/response models for inputset CRUD operations.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from harness_python_sdk.base_model import HarnessModel


class InputSetV0Response(HarnessModel):
    """Inputset resource response model."""

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
    stages: list[dict] | None = []
    variables: list[dict] | None = []


class InputSetV0ListResponse(HarnessModel):
    """InputSet resource response list model."""

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
    input_set_type: str = Field(..., alias="inputSetType")
    store_type: str = Field(default=None, alias="storeType")
    is_inline_hc_entity: bool = Field(default=False, alias="isInlineHCEntity")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastUpdatedAt")


class InputSetV0CreateRequest(HarnessModel):
    """Inputset creation request model."""

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
    stages: list[dict] | None = []
    variables: list[dict] | None = []
