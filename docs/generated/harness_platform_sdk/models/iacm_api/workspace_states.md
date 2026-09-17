Module harness_platform_sdk.models.iacm_api.workspace_states
============================================================
Workspacestate resource models for Harness SDK.

Defines request/response models for workspacestate CRUD operations.

Classes
-------

`WorkspaceStateCreateRequest(**data: Any)`
:   Workspacestate creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `check_results: list | None`
    :   The type of the None singleton.

    `lineage: str | None`
    :   The type of the None singleton.

    `outputs: dict | None`
    :   The type of the None singleton.

    `resources: list | None`
    :   The type of the None singleton.

    `serial: int | None`
    :   The type of the None singleton.

    `terraform_version: str`
    :   The type of the None singleton.

    `version: int | None`
    :   The type of the None singleton.

`WorkspaceStateResponse(**data: Any)`
:   Workspacestate resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `check_results: list | None`
    :   The type of the None singleton.

    `lineage: str | None`
    :   The type of the None singleton.

    `outputs: dict | None`
    :   The type of the None singleton.

    `resources: list | None`
    :   The type of the None singleton.

    `serial: int | None`
    :   The type of the None singleton.

    `terraform_version: str`
    :   The type of the None singleton.

    `version: int | None`
    :   The type of the None singleton.