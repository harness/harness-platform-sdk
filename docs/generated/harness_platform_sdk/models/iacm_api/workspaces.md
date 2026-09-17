Module harness_platform_sdk.models.iacm_api.workspaces
======================================================
Workspace resource models for Harness SDK.

Defines request/response models for workspace CRUD operations.

Classes
-------

`WorkspaceCore(**data: Any)`
:   Workspace resource cor model.
    
    Used as root for all models.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Descendants

    * harness_platform_sdk.models.iacm_api.workspaces.WorkspaceCreateRequest
    * harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse

    ### Class variables

    `account_identifier: str`
    :   The type of the None singleton.

    `cost_estimation_enabled: bool | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `default_pipelines: dict | None`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `environment_variables: dict | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `provider_connector: str | None`
    :   The type of the None singleton.

    `provider_connectors: list[dict] | None`
    :   The type of the None singleton.

    `provisioner: str`
    :   The type of the None singleton.

    `provisioner_configuration: dict | None`
    :   The type of the None singleton.

    `provisioner_version: str | None`
    :   The type of the None singleton.

    `prune_sensitive_data: bool | None`
    :   The type of the None singleton.

    `repository: str | None`
    :   The type of the None singleton.

    `repository_branch: str | None`
    :   The type of the None singleton.

    `repository_commit: str | None`
    :   The type of the None singleton.

    `repository_connector: str | None`
    :   The type of the None singleton.

    `repository_path: str | None`
    :   The type of the None singleton.

    `repository_sha: str | None`
    :   The type of the None singleton.

    `repository_submodules: str | None`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `terraform_variable_files: list[dict] | None`
    :   The type of the None singleton.

    `terraform_variables: dict | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `variable_sets: list[str] | None`
    :   The type of the None singleton.

`WorkspaceCreateRequest(**data: Any)`
:   Workspace creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.iacm_api.workspaces.WorkspaceCore
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Methods

    `check_at_least_one(self) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceCreateRequest`
    :   Validator for check_at_least_one.
        
        Returns:
            Validated value.

`WorkspaceResponse(**data: Any)`
:   Workspace resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.iacm_api.workspaces.WorkspaceCore
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `backend_locked: bool | None`
    :   The type of the None singleton.

    `budget: float | None`
    :   The type of the None singleton.

    `cost_breakdown_json: dict | str | None`
    :   The type of the None singleton.

    `cost_diff_json: dict | str | None`
    :   The type of the None singleton.

    `modules_json: str | None`
    :   The type of the None singleton.

    `providers_json: dict | None`
    :   The type of the None singleton.

    `status: str | None`
    :   The type of the None singleton.

    ### Static methods

    `normalize_providers_json(v)`
    :   Validator for normalize_providers_json.
        
        Args:
            v: Parameter.
        
        Returns:
            Validated value.