"""
Score resource models for Harness SDK.

Defines request/response models for scores CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel


class ScoreResponse(HarnessModel):
    """Score resource response model.

    Used for both list() and get_aggregated_scores() item responses.
    """

    identifier: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    #####
    # Additional Response properties
    #####
    kind: str
    overall_score: int
    scorecard_scores: list[dict] | None = []

class ScoreSummaryResponse(HarnessModel):
    """Score summary resource response model.

    Used for get() item response.
    """

    identifier: str
    kind: str
    scorecard_identifier: str
    scorecard_name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    #####
    # Additional Response properties
    #####
    description: str | None = None
    recalibrate_info: dict | None = {}
    # overall_score: int
    checks_statuses: list[dict] | None = []
    timestamp: int

class ScoreCreateRequest(HarnessModel):
    """Score creation request model."""

    identifier: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    #####
    # Additional Response properties
    #####
    kind: str
