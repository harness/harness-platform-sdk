Module harness_platform_sdk.base_model
======================================
Base model for all Harness SDK domain models.

HarnessModel is the base class for all request/response models in the SDK.
It allows extra fields and populates by name or alias.

Classes
-------

`HarnessModel(**data: Any)`
:   Base model for Harness SDK domain models.
    
    Allows extra fields (for forward compatibility) and supports
    population by field name or alias.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Descendants

    * harness_platform_sdk.models.authz.resource_groups.ResourceGroupCreateRequest
    * harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse
    * harness_platform_sdk.models.authz.role_assignments.RoleAssignmentCreateRequest
    * harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse
    * harness_platform_sdk.models.authz.roles.RoleCreateRequest
    * harness_platform_sdk.models.authz.roles.RoleResponse
    * harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalCreateRequest
    * harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalListResponse
    * harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalResponse
    * harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineCreateRequest
    * harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse
    * harness_platform_sdk.models.iacm_api.workspace_states.WorkspaceStateCreateRequest
    * harness_platform_sdk.models.iacm_api.workspace_states.WorkspaceStateResponse
    * harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableCreateRequest
    * harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse
    * harness_platform_sdk.models.iacm_api.workspaces.WorkspaceCore
    * harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse
    * harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponseByEntity
    * harness_platform_sdk.models.idp_api.entities.EntityCreateRequest
    * harness_platform_sdk.models.idp_api.entities.EntityResponse
    * harness_platform_sdk.models.idp_api.scores.ScoreCreateRequest
    * harness_platform_sdk.models.idp_api.scores.ScoreResponse
    * harness_platform_sdk.models.idp_api.scores.ScoreSummaryResponse
    * harness_platform_sdk.models.ng_api.connectors.ConnectorCreateRequest
    * harness_platform_sdk.models.ng_api.connectors.ConnectorResponse
    * harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2CreateRequest
    * harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response
    * harness_platform_sdk.models.ng_api.infrastructures.InfrastructureCreateRequest
    * harness_platform_sdk.models.ng_api.infrastructures.InfrastructureResponse
    * harness_platform_sdk.models.ng_api.organizations.OrganizationCreateRequest
    * harness_platform_sdk.models.ng_api.organizations.OrganizationResponse
    * harness_platform_sdk.models.ng_api.projects.ProjectCreateRequest
    * harness_platform_sdk.models.ng_api.projects.ProjectResponse
    * harness_platform_sdk.models.ng_api.secrets.SecretCreateRequest
    * harness_platform_sdk.models.ng_api.secrets.SecretResponse
    * harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideApiCreateRequest
    * harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideApiSpec
    * harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideCreateRequest
    * harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse
    * harness_platform_sdk.models.ng_api.services.ServiceCreateRequest
    * harness_platform_sdk.models.ng_api.services.ServiceResponse
    * harness_platform_sdk.models.ng_api.user_groups.UserGroupCreateRequest
    * harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse
    * harness_platform_sdk.models.ng_api.variables.VariableCore
    * harness_platform_sdk.models.ng_api.variables.VariableSpec
    * harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0CreateRequest
    * harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0ListResponse
    * harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0Response
    * harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0CreateRequest
    * harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0ListResponse
    * harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0Response
    * harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0CreateRequest
    * harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0ListResponse
    * harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response
    * harness_platform_sdk.models.template_api.templates_v0.TemplateV0Core

    ### Class variables

    `model_config`
    :   The type of the None singleton.