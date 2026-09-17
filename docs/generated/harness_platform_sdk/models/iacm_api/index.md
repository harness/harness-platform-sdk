Module harness_platform_sdk.models.iacm_api
===========================================
Harness models for /ng/api/ resources.

Domain-specific request and response models for P2 and P1 managers.

Sub-modules
-----------
* harness_platform_sdk.models.iacm_api.workspace_approvals
* harness_platform_sdk.models.iacm_api.workspace_default_pipelines
* harness_platform_sdk.models.iacm_api.workspace_states
* harness_platform_sdk.models.iacm_api.workspace_variables
* harness_platform_sdk.models.iacm_api.workspaces

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

`WorkspaceDefaultPipelineCreateRequest(**data: Any)`
:   WorkspaceDefaultPipeline creation request model.
    
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

    `operation: harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineOperation`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `provisioner: harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineProvisioner`
    :   The type of the None singleton.

    `workspace_identifier: str`
    :   The type of the None singleton.

`WorkspaceDefaultPipelineOperation(*values)`
:   Terraform operation type for workspace pipelines.
    
    Attributes:
        plan: Plan (dry-run) operation.
        apply: Apply (execute) operation.
        destroy: Destroy (cleanup) operation.
        drift: Drift detection operation.
        synth: Synthesize operation.
        diff: Diff operation.
        deploy: Deploy operation.

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `apply`
    :   The type of the None singleton.

    `deploy`
    :   The type of the None singleton.

    `destroy`
    :   The type of the None singleton.

    `diff`
    :   The type of the None singleton.

    `drift`
    :   The type of the None singleton.

    `plan`
    :   The type of the None singleton.

    `synth`
    :   The type of the None singleton.

`WorkspaceDefaultPipelineProvisioner(*values)`
:   Infrastructure provisioning tool type.
    
    Attributes:
        terraform: Terraform provisioner.
        opentofu: OpenTofu provisioner (Terraform fork).
        terragrunt: Terragrunt provisioner.
        awscdk: AWS CDK provisioner.

    ### Ancestors (in MRO)

    * builtins.str
    * enum.Enum

    ### Class variables

    `awscdk`
    :   The type of the None singleton.

    `opentofu`
    :   The type of the None singleton.

    `terraform`
    :   The type of the None singleton.

    `terragrunt`
    :   The type of the None singleton.

`WorkspaceDefaultPipelineResponse(**data: Any)`
:   WorkspaceDefaultPipeline resource response model.
    
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

    `operation: harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineOperation`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `pipeline_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    `workspace_identifier: str`
    :   The type of the None singleton.

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

`WorkspaceStateCreateRequest(**data: Any)`
:   Workspacestate creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `check_results: list | None`
    :   The type of the None singleton.

    `lineage: str | None`
    :   The type of the None singleton.

    `outputs: dict | None`
    :   The type of the None singleton.

    `resources: list | None`
    :   The type of the None singleton.

    `serial: int | None`
    :   The type of the None singleton.

    `terraform_version: str`
    :   The type of the None singleton.

    `version: int | None`
    :   The type of the None singleton.

`WorkspaceStateResponse(**data: Any)`
:   Workspacestate resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `check_results: list | None`
    :   The type of the None singleton.

    `lineage: str | None`
    :   The type of the None singleton.

    `outputs: dict | None`
    :   The type of the None singleton.

    `resources: list | None`
    :   The type of the None singleton.

    `serial: int | None`
    :   The type of the None singleton.

    `terraform_version: str`
    :   The type of the None singleton.

    `version: int | None`
    :   The type of the None singleton.

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