"""
Pipeline resource models for Harness SDK.

Defines request/response models for pipeline CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class PipelineResponse(HarnessModel):
    """Pipeline resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    org: str | None = None
    project: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None
    modules: list[str] | None = None
    created: int | None = None
    updated: int | None = None
    pipeline_yaml: str | None = Field(None, alias="pipelineYaml")
    template_applied_pipeline_yaml: str | None = Field(None, alias="templateAppliedPipelineYaml")
    git_details: dict | None = Field(None, alias="gitDetails")
    valid: bool | None = None
    connector_ref: str | None = Field(None, alias="connectorRef")
    store_type: str | None = Field(None, alias="storeType")
    yaml_version: str | None = Field(None, alias="yamlVersion")


class PipelineCreateRequest(HarnessModel):
    """Pipeline creation request model."""

    identifier: str
    name: str
    pipeline_yaml: str
    org: str | None = None
    project: str | None = None
    description: str | None = None
    tags: dict[str, str] | None = None


class PipelineUpdateRequest(HarnessModel):
    """Pipeline update request model."""

    identifier: str
    name: str
    pipeline_yaml: str
    description: str | None = None
    tags: dict[str, str] | None = None
