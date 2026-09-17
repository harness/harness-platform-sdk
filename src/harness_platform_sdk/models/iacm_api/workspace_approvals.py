"""WorkspaceApproval resource models for Harness SDK.

Defines request/response models for workspaceapproval CRUD operations.
"""

from __future__ import annotations

from enum import Enum

from pydantic import AliasChoices, Field

from harness_platform_sdk.base_model import HarnessModel


class WorkspaceApprovalStatus(str, Enum):
    """Status of a workspace approval request.

    Attributes:
        approved: Request was approved.
        rejected: Request was rejected.
        pending: Approval is pending.
        unknown: Status is unknown or unrecognized.
    """

    approved = "approved"
    rejected = "rejected"
    pending = "pending"
    unknown = "unknown"


class WorkspaceApprovalListResponse(HarnessModel):
    """WorkspaceApproval resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str = Field(default=None, alias="id")
    account_identifier: str = Field(
        default=None, alias=AliasChoices("account", "accountIdentifier")
    )
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    workspace_id: str
    pipeline_stage_id: str
    pipeline_execution_id: str
    status: WorkspaceApprovalStatus
    actioned_by: str | None = None
    actioned_by_email: str | None = None
    created_at: int = Field(default=None, alias="created")
    updated_at: int = Field(default=None, alias="updated")


class WorkspaceApprovalResponse(HarnessModel):
    """Model for WorkspaceApprovalResponse."""

    status: WorkspaceApprovalStatus
    actioned_by: str | None = None
    actioned_by_email: str | None = None
    created_at: int = Field(default=None, alias="created")
    updated_at: int = Field(default=None, alias="updated")


class WorkspaceApprovalCreateRequest(HarnessModel):
    """WorkspaceApproval creation request model."""

    identifier: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}
    #####
    # Additional Response properties
    #####
    status: WorkspaceApprovalStatus
    actioned_by: str
    actioned_by_email: str
