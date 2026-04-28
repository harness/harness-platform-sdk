"""
Variable resource models for Harness SDK.

Defines request/response models for variable CRUD operations.
"""

from __future__ import annotations

from pydantic import Field

from harness_python_sdk.base_model import HarnessModel, BaseModel

class VariableSpec(HarnessModel):
    value_type: str = Field(default="FIXED", alias="valueType")
    type: str | None ="string"
    fixed_value: str = Field(..., alias="fixedValue")

class VariableCore(HarnessModel):
    """Variable resource cor model.

    Used as root for all models.
    """

    identifier: str
    name: str
    account_identifier: str = Field(default=None, alias="accountIdentifier")
    org_identifier: str = Field(default=None, alias="orgIdentifier")
    project_identifier: str = Field(default=None, alias="projectIdentifier")
    description: str | None = None
    tags: dict[str, str] | None = {}

    created_at: int = Field(default=None, alias="createdAt")
    updated_at: int = Field(default=None, alias="updatedAt")

    type: str | None = "String"
    spec: VariableSpec | None = None

class VariableResponse(VariableCore):
    """Variable resource response model.

    Used for both get() and list() item responses.
    """


class VariableCreateRequest(VariableCore):
    """Variable creation request model."""

    type: str
    spec: VariableSpec
