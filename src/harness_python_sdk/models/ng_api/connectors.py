"""
Connector resource models for Harness SDK.

Defines request/response models for connector CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class ConnectorResponse(HarnessModel):
    """Connector resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    spec: dict | None = None
    status: dict | None = None
    harness_managed: bool | None = Field(None, alias="harnessManagedConnector")
    governance_metadata: dict | None = Field(None, alias="governanceMetadata")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastModifiedAt")


class ConnectorCreateRequest(HarnessModel):
    """Connector creation request model."""

    identifier: str
    name: str
    spec: dict
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
