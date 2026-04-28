"""
Workspacestate resource models for Harness SDK.

Defines request/response models for workspacestate CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class WorkspaceStateResponse(HarnessModel):
    """Workspacestate resource response model.

    Used for both get() and list() item responses.
    """

    check_results: list | None = []
    lineage: str | None = None
    outputs: dict | None = {}
    resources: list | None = []
    terraform_version: str
    serial: int | None = 0
    version: int | None = 0


class WorkspaceStateCreateRequest(HarnessModel):
    """Workspacestate creation request model."""

    check_results: list | None = []
    lineage: str | None = None
    outputs: dict | None = {}
    resources: list | None = []
    terraform_version: str
    serial: int | None = 0
    version: int | None = 0
