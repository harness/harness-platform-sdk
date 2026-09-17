Module harness_platform_sdk.models.iacm_api.workspace_approvals
===============================================================
WorkspaceApproval resource models for Harness SDK.

Defines request/response models for workspaceapproval CRUD operations.

Classes
-------

`WorkspaceApprovalCreateRequest(**data: Any)`
:   WorkspaceApproval creation request model.
    
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

    `actioned_by: str`
    :   The type of the None singleton.

    `actioned_by_email: str`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `status: harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalStatus`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`WorkspaceApprovalListResponse(**data: Any)`
:   WorkspaceApproval resource response model.
    
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

    `actioned_by: str | None`
    :   The type of the None singleton.

    `actioned_by_email: str | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_execution_id: str`
    :   The type of the None singleton.

    `pipeline_stage_id: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `status: harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalStatus`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `workspace_id: str`
    :   The type of the None singleton.

`WorkspaceApprovalResponse(**data: Any)`
:   Model for WorkspaceApprovalResponse.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `actioned_by: str | None`
    :   The type of the None singleton.

    `actioned_by_email: str | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `status: harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalStatus`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`WorkspaceApprovalStatus(*values)`
:   Status of a workspace approval request.
    
    Attributes:
        approved: Request was approved.
        rejected: Request was rejected.
        pending: Approval is pending.
        unknown: Status is unknown or unrecognized.

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `approved`
    :   The type of the None singleton.

    `pending`
    :   The type of the None singleton.

    `rejected`
    :   The type of the None singleton.

    `unknown`
    :   The type of the None singleton.