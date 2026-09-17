Module harness_platform_sdk.models.iacm_api.workspace_default_pipelines
=======================================================================
WorkspaceDefaultPipeline resource models for Harness SDK.

Defines request/response models for workspacedefaultpipelines CRUD operations.

Classes
-------

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