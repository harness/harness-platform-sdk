Module harness_platform_sdk.models.pipeline_api.pipelines_v0
============================================================
Pipeline resource models for Harness SDK.

Defines request/response models for pipeline CRUD operations.

Classes
-------

`PipelineV0CreateRequest(**data: Any)`
:   Pipeline creation request model.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `stages: list[dict]`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `variables: list[dict] | None`
    :   The type of the None singleton.

`PipelineV0ListResponse(**data: Any)`
:   Pipeline resource response list model.
    
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

    `modules: list[str]`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `num_of_stages: int`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `recent_executions_info: list[dict]`
    :   The type of the None singleton.

    `stage_names: list[str]`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `version: int`
    :   The type of the None singleton.

    `yaml_version: int`
    :   The type of the None singleton.

`PipelineV0Response(**data: Any)`
:   Pipeline resource response model.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `stages: list[dict]`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.