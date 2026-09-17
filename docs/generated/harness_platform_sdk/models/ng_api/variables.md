Module harness_platform_sdk.models.ng_api.variables
===================================================
Variable resource models for Harness SDK.

Defines request/response models for variable CRUD operations.

Classes
-------

`VariableCore(**data: Any)`
:   Variable resource cor model.
    
    Used as root for all models.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Descendants

    * harness_platform_sdk.models.ng_api.variables.VariableCreateRequest
    * harness_platform_sdk.models.ng_api.variables.VariableResponse

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `spec: harness_platform_sdk.models.ng_api.variables.VariableSpec | None`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`VariableCreateRequest(**data: Any)`
:   Variable creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.ng_api.variables.VariableCore
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

`VariableResponse(**data: Any)`
:   Variable resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.ng_api.variables.VariableCore
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

`VariableSpec(**data: Any)`
:   Model for VariableSpec.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `fixed_value: str`
    :   The type of the None singleton.

    `type: str | None`
    :   The type of the None singleton.

    `value_type: str`
    :   The type of the None singleton.