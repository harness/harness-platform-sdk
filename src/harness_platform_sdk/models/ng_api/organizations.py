"""Organization resource models for Harness SDK.

Defines request/response models for organization CRUD operations.
"""

from __future__ import annotations

from pydantic import Field, field_validator

from harness_platform_sdk.base_model import HarnessModel


class OrganizationResponse(HarnessModel):
    """Organization resource response model.

    Used for both get() and list() item responses.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = None
    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="lastModifiedAt")
    harness_managed: bool | None = Field(None, alias="harnessManaged")

    @field_validator("created_at", mode="before")
    @classmethod
    def allow_null_string(cls, v):
        """Validator for allow_null_string.

        Args:
            v: Parameter.

        Returns:
            Validated value.
        """
        if v == "null" or v is None:
            return 0
        return v


class OrganizationCreateRequest(HarnessModel):
    """Organization creation request model."""

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = None
