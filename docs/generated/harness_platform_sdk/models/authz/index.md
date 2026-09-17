Module harness_platform_sdk.models.authz
========================================
Harness models for /authz/ resources.

Domain-specific request and response models.

Sub-modules
-----------
* harness_platform_sdk.models.authz.resource_groups
* harness_platform_sdk.models.authz.role_assignments
* harness_platform_sdk.models.authz.roles

Classes
-------

`ResourceGroupCreateRequest(**data: Any)`
:   Resource Group creation request model.
    
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

    `allowed_scope_levels: list[str]`
    :   The type of the None singleton.

    `color: str | None`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `included_scopes: list[dict]`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `resource_filter: dict | None`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`ResourceGroupResponse(**data: Any)`
:   Resource Group resource response model.
    
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

    `allowed_scope_levels: list[str]`
    :   The type of the None singleton.

    `color: str | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `included_scopes: list[dict]`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `resource_filter: dict | None`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

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

`RoleCreateRequest(**data: Any)`
:   Role creation request model.
    
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

    `allowed_scope_levels: list[str]`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `permissions: list[str] | None`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`RoleResponse(**data: Any)`
:   Role resource response model.
    
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

    `allowed_scope_levels: list[str]`
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

    `permissions: list[str] | None`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.