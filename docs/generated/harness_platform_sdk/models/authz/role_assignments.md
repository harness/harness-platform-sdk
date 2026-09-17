Module harness_platform_sdk.models.authz.role_assignments
=========================================================
Role Assignment resource models for Harness SDK.

Defines request/response models for role assignment CRUD operations.

Classes
-------

`RoleAssignmentCreateRequest(**data: Any)`
:   Role Assignment creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `disabled: bool | None`
    :   The type of the None singleton.

    `identifier: str | None`
    :   The type of the None singleton.

    `principal: dict`
    :   The type of the None singleton.

    `resource_group_identifier: str`
    :   The type of the None singleton.

    `role_identifier: str`
    :   The type of the None singleton.

    `role_reference: dict`
    :   The type of the None singleton.

`RoleAssignmentResponse(**data: Any)`
:   Role Assignment resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `created: int | None`
    :   The type of the None singleton.

    `disabled: bool | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `principal: dict`
    :   The type of the None singleton.

    `resource_group_identifier: str`
    :   The type of the None singleton.

    `role_identifier: str`
    :   The type of the None singleton.

    `role_reference: dict`
    :   The type of the None singleton.

    `updated: int | None`
    :   The type of the None singleton.