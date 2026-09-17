"""CatalogCustomProperty resource models for Harness SDK.

Defines request/response models for catalogcustomproperties CRUD operations.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from harness_platform_sdk.base_model import HarnessModel


class CatalogCustomPropertyResponse(HarnessModel):
    """CatalogCustomProperty resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    #####
    # Additional Response properties
    #####
    kind: str
    mode: str
    catalog_property: str
    value: Any = Field(default=None, description="Can be anything")


class CatalogCustomPropertyResponseByEntity(HarnessModel):
    """CatalogCustomProperty resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    #####
    # Additional Response properties
    #####
    kind: str
    properties: list[dict]


class CatalogCustomPropertyCreateRequest(CatalogCustomPropertyResponse):
    """CatalogCustomProperty creation request model."""

    #####
    # Additional Response properties
    #####
