Module harness_platform_sdk.models.ng_api.services
==================================================
Service resource models for Harness SDK.

Defines request/response models for service CRUD operations.

Classes
-------

`ServiceCreateRequest(**data: Any)`
:   Service creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `artifacts: dict | None`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `is_v2_service: bool`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`ServiceResponse(**data: Any)`
:   Service resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `artifacts: dict | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `is_v2_service: bool`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.