"""ServiceOverride resource models for Harness SDK.

Defines request/response models for serviceoverride CRUD operations.
"""

from __future__ import annotations

from pydantic import AliasChoices, Field

from harness_platform_sdk.base_model import HarnessModel


class ServiceOverrideResponse(HarnessModel):
    """ServiceOverride resource response model (V2).

    Used for both get() and list() item responses.
    """

    identifier: str | None = None
    account_id: str | None = Field(default=None, alias="accountId")
    org_identifier: str | None = Field(default=None, alias="orgIdentifier")
    project_identifier: str | None = Field(default=None, alias="projectIdentifier")
    environment_identifier: str | None = Field(
        default=None, alias=AliasChoices("environmentRef", "environment_ref")
    )
    service_identifier: str | None = Field(
        default=None, alias=AliasChoices("serviceRef", "service_ref")
    )
    infra_identifier: str | None = Field(
        default=None, alias=AliasChoices("infraIdentifier", "infra_identifier")
    )
    override_type: str | None = Field(default=None, alias="type")
    application_settings: dict | None = Field(default=None, alias="applicationSettings")
    environment_variables: list[dict] | None = Field(default=None, alias="cliEnvironmentVariables")
    config_files: list[dict] | None = Field(default=None, alias="configFiles")
    connection_strings: dict | None = Field(default=None, alias="connectionStrings")
    manifests: list[dict] | None = Field(default=None, alias="manifests")
    variables: list[dict] | None = Field(default=None, alias="variables")


class ServiceOverrideCreateRequest(HarnessModel):
    """ServiceOverride creation request model (V2)."""

    org_identifier: str | None = Field(default=None, alias="orgIdentifier")
    project_identifier: str | None = Field(default=None, alias="projectIdentifier")
    environment_ref: str | None = Field(default=None, alias="environmentRef")
    service_ref: str | None = Field(default=None, alias="serviceRef")
    infra_identifier: str | None = Field(default=None, alias="infraIdentifier")
    override_type: str | None = None
    application_settings: dict | None = Field(default={}, alias="applicationSettings")
    environment_variables: list[dict] | None = Field(default=[], alias="cliEnvironmentVariables")
    config_files: list[dict] | None = Field(default=[], alias="configFiles")
    connection_strings: dict | None = Field(default={}, alias="connectionStrings")
    manifests: list[dict] | None = Field(default=[], alias="manifests")
    variables: list[dict] | None = Field(default=[], alias="variables")


class ServiceOverrideApiSpec(HarnessModel):
    """Nested spec for ServiceOverride creation request."""

    applicationSettings: dict | None = Field(default=None, alias="application_settings")
    cliEnvironmentVariables: list[dict] | None = Field(default=None, alias="environment_variables")
    configFiles: list[dict] | None = Field(default=None, alias="config_files")
    connectionStrings: dict | None = Field(default=None, alias="connection_strings")
    manifests: list[dict] | None = Field(default=None, alias="manifests")
    variables: list[dict] | None = Field(default=None, alias="variables")


class ServiceOverrideApiCreateRequest(HarnessModel):
    """ServiceOverride creation request model (V2)."""

    orgIdentifier: str | None = Field(default=None, alias="org_identifier")
    projectIdentifier: str | None = Field(default=None, alias="project_identifier")
    environmentRef: str | None = Field(default=None, alias="environment_identifier")
    serviceRef: str | None = Field(default=None, alias="service_identifier")
    infraIdentifier: str | None = Field(default=None, alias="infra_identifier")
    type: str | None = Field(default=None, alias="override_type")
    spec: ServiceOverrideApiSpec | None = Field(default=None, alias="spec")
