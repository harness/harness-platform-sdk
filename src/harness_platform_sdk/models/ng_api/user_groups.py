"""UserGroup resource models for Harness SDK.

Defines request/response models for user_group CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_platform_sdk.base_model import HarnessModel


class UserGroupResponse(HarnessModel):
    """UserGroup resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    users: list[str] | None = []
    notification_configs: list[dict] = Field(default=None, alias="notificationConfigs")

    linked_sso_id: str = Field(default=None, alias="linkedSsoId")
    linked_sso_display_name: str = Field(default=None, alias="linkedSsoDisplayName")
    linked_sso_type: str = Field(default=None, alias="linkedSsoType")
    sso_group_id: str = Field(default=None, alias="ssoGroupId")
    sso_group_name: str = Field(default=None, alias="ssoGroupName")

    harness_managed: bool = Field(default=False, alias="harnessManaged")
    sso_linked: bool = Field(default=False, alias="ssoLinked")
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updatedAt")


class UserGroupCreateRequest(HarnessModel):
    """UserGroup creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    users: list[str] | None = []
    notification_configs: list[dict] = Field(default=None, alias="notificationConfigs")

    linked_sso_id: str = Field(default=None, alias="linkedSsoId")
    linked_sso_display_name: str = Field(default=None, alias="linkedSsoDisplayName")
    linked_sso_type: str = Field(default=None, alias="linkedSsoType")
    sso_group_id: str = Field(default=None, alias="ssoGroupId")
    sso_group_name: str = Field(default=None, alias="ssoGroupName")

    harness_managed: bool = Field(default=False, alias="harnessManaged")
    sso_linked: bool = Field(default=False, alias="ssoLinked")
