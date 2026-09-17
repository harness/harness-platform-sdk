Module harness_platform_sdk.models.ng_api.service_overrides
===========================================================
ServiceOverride resource models for Harness SDK.

Defines request/response models for serviceoverride CRUD operations.

Classes
-------

`ServiceOverrideApiCreateRequest(**data: Any)`
:   ServiceOverride creation request model (V2).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `environmentRef: str | None`
    :   The type of the None singleton.

    `infraIdentifier: str | None`
    :   The type of the None singleton.

    `orgIdentifier: str | None`
    :   The type of the None singleton.

    `projectIdentifier: str | None`
    :   The type of the None singleton.

    `serviceRef: str | None`
    :   The type of the None singleton.

    `spec: harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideApiSpec | None`
    :   The type of the None singleton.

    `type: str | None`
    :   The type of the None singleton.

`ServiceOverrideApiSpec(**data: Any)`
:   Nested spec for ServiceOverride creation request.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `applicationSettings: dict | None`
    :   The type of the None singleton.

    `cliEnvironmentVariables: list[dict] | None`
    :   The type of the None singleton.

    `configFiles: list[dict] | None`
    :   The type of the None singleton.

    `connectionStrings: dict | None`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `variables: list[dict] | None`
    :   The type of the None singleton.

`ServiceOverrideCreateRequest(**data: Any)`
:   ServiceOverride creation request model (V2).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `application_settings: dict | None`
    :   The type of the None singleton.

    `config_files: list[dict] | None`
    :   The type of the None singleton.

    `connection_strings: dict | None`
    :   The type of the None singleton.

    `environment_ref: str | None`
    :   The type of the None singleton.

    `environment_variables: list[dict] | None`
    :   The type of the None singleton.

    `infra_identifier: str | None`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `org_identifier: str | None`
    :   The type of the None singleton.

    `override_type: str | None`
    :   The type of the None singleton.

    `project_identifier: str | None`
    :   The type of the None singleton.

    `service_ref: str | None`
    :   The type of the None singleton.

    `variables: list[dict] | None`
    :   The type of the None singleton.

`ServiceOverrideResponse(**data: Any)`
:   ServiceOverride resource response model (V2).
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `account_id: str | None`
    :   The type of the None singleton.

    `application_settings: dict | None`
    :   The type of the None singleton.

    `config_files: list[dict] | None`
    :   The type of the None singleton.

    `connection_strings: dict | None`
    :   The type of the None singleton.

    `environment_identifier: str | None`
    :   The type of the None singleton.

    `environment_variables: list[dict] | None`
    :   The type of the None singleton.

    `identifier: str | None`
    :   The type of the None singleton.

    `infra_identifier: str | None`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `org_identifier: str | None`
    :   The type of the None singleton.

    `override_type: str | None`
    :   The type of the None singleton.

    `project_identifier: str | None`
    :   The type of the None singleton.

    `service_identifier: str | None`
    :   The type of the None singleton.

    `variables: list[dict] | None`
    :   The type of the None singleton.