"""
TemplateV0 resource models for Harness SDK.

Defines request/response models for template CRUD operations.
"""

from __future__ import annotations

from pydantic import Field, AliasChoices

from harness_python_sdk.base_model import HarnessModel

class TemplateV0Core(HarnessModel):
    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias=AliasChoices("accountId","accountIdentifier"))
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastUpdatedAt")


class TemplateV0Response(TemplateV0Core):
    """TemplateV0 resource response model.

    Used for both get() and list() item responses.
    """
    child_type: str = Field(default=None, alias="childType")
    entity_validity_details: dict = Field(default={}, alias="entityValidityDetails")
    git_details: dict = Field(default={},alias="gitDetails")
    is_inline_hc_entity: bool = Field(default=False, alias="isInlineHCEntity")
    updated_at: int = Field(default=None, alias="lastUpdatedAt")
    stable_template: bool = Field(default=False, alias="stableTemplate")
    store_type: str = Field(default=None, alias="storeType")

    template_entity_type: str = Field(..., alias="templateEntityType")
    template_scope: str = Field(default="unknown", alias="templateScope")
    template_spec: dict = Field(default={}, alias="template_spec")

    version: int
    version_label: str = Field(..., alias="versionLabel")
    yaml_version: int = Field(default=0, alias="yamlVersion")

class TemplateV0CreateRequest(TemplateV0Core):
    """TemplateV0 creation request model."""

    git_details: dict = Field(default={},alias="gitDetails")
    store_type: str = Field(default="INLINE", alias="storeType")
    template_entity_type: str = Field(..., alias="templateEntityType")
    template_spec: dict = Field(..., alias="template_spec")
    version_label: str
