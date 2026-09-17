Module harness_platform_sdk.models.pipeline_api.triggers_v0
===========================================================
Trigger resource models for Harness SDK.

Defines request/response models for trigger CRUD operations.

Classes
-------

`TriggerV0CreateRequest(**data: Any)`
:   Trigger creation request model.
    
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

    `enabled: bool | None`
    :   The type of the None singleton.

    `encrypted_webhook_secret_identifier: str`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `inputs: dict | None`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `source: dict | None`
    :   The type of the None singleton.

    `stages_to_execute: list[str]`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`TriggerV0ListResponse(**data: Any)`
:   Trigger resource response model.
    
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

    `enable_dag: bool`
    :   The type of the None singleton.

    `entity_validity_details: dict`
    :   The type of the None singleton.

    `execution_summary_info: dict`
    :   The type of the None singleton.

    `git_details: dict[str, dict]`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `is_draft: bool`
    :   The type of the None singleton.

    `is_inline_hc_entity: bool`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `num_of_stages: int`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `recent_executions_info: list[str]`
    :   The type of the None singleton.

    `stage_names: list[str]`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `yaml_version: int`
    :   The type of the None singleton.

`TriggerV0Response(**data: Any)`
:   Trigger resource response model.
    
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

    `enabled: bool | None`
    :   The type of the None singleton.

    `encrypted_webhook_secret_identifier: str`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `inputs: dict | None`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `source: dict | None`
    :   The type of the None singleton.

    `stages_to_execute: list[str]`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `webhook_url: str`
    :   The type of the None singleton.