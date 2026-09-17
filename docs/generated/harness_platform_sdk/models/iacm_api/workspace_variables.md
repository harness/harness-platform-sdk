Module harness_platform_sdk.models.iacm_api.workspace_variables
===============================================================
WorkspaceVariable resource models for Harness SDK.

Defines request/response models for workspacevariables CRUD operations.

Classes
-------

`WorkspaceValueType(*values)`
:   Value type for workspace variables.
    
    Attributes:
        string: Plain string value.
        secret: Secret/sensitive value (redacted from logs).

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `secret`
    :   The type of the None singleton.

    `string`
    :   The type of the None singleton.

`WorkspaceVariableCreateRequest(**data: Any)`
:   WorkspaceVariable creation request model.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `kind: harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableKind`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `value: str`
    :   The type of the None singleton.

    `value_type: harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceValueType`
    :   The type of the None singleton.

    `workspace_identifier: str`
    :   The type of the None singleton.

`WorkspaceVariableKind(*values)`
:   Variable kind/scope for workspace variables.
    
    Attributes:
        env: Environment variable scope.
        tf: Terraform variable scope.

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `env`
    :   The type of the None singleton.

    `tf`
    :   The type of the None singleton.

`WorkspaceVariableResponse(**data: Any)`
:   WorkspaceVariable resource response model.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `kind: harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableKind`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `value: str`
    :   The type of the None singleton.

    `value_type: harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceValueType`
    :   The type of the None singleton.

    `workspace_identifier: str`
    :   The type of the None singleton.