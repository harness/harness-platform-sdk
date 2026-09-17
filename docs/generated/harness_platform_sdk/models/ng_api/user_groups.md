Module harness_platform_sdk.models.ng_api.user_groups
=====================================================
UserGroup resource models for Harness SDK.

Defines request/response models for user_group CRUD operations.

Classes
-------

`UserGroupCreateRequest(**data: Any)`
:   UserGroup creation request model.
    
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

    `description: str | None`
    :   The type of the None singleton.

    `harness_managed: bool`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `linked_sso_display_name: str`
    :   The type of the None singleton.

    `linked_sso_id: str`
    :   The type of the None singleton.

    `linked_sso_type: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `notification_configs: list[dict]`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `sso_group_id: str`
    :   The type of the None singleton.

    `sso_group_name: str`
    :   The type of the None singleton.

    `sso_linked: bool`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `users: list[str] | None`
    :   The type of the None singleton.

`UserGroupResponse(**data: Any)`
:   UserGroup resource response model.
    
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

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `harness_managed: bool`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `linked_sso_display_name: str`
    :   The type of the None singleton.

    `linked_sso_id: str`
    :   The type of the None singleton.

    `linked_sso_type: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `notification_configs: list[dict]`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `sso_group_id: str`
    :   The type of the None singleton.

    `sso_group_name: str`
    :   The type of the None singleton.

    `sso_linked: bool`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `users: list[str] | None`
    :   The type of the None singleton.