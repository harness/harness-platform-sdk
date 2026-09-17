Module harness_platform_sdk.models.ng_api
=========================================
Harness models for /ng/api/ resources.

Domain-specific request and response models for P2 and P1 managers.

Sub-modules
-----------
* harness_platform_sdk.models.ng_api.connectors
* harness_platform_sdk.models.ng_api.environments_v2
* harness_platform_sdk.models.ng_api.infrastructures
* harness_platform_sdk.models.ng_api.organizations
* harness_platform_sdk.models.ng_api.projects
* harness_platform_sdk.models.ng_api.secrets
* harness_platform_sdk.models.ng_api.service_overrides
* harness_platform_sdk.models.ng_api.services
* harness_platform_sdk.models.ng_api.user_groups
* harness_platform_sdk.models.ng_api.variables

Classes
-------

`ConnectorCreateRequest(**data: Any)`
:   Connector creation request model.
    
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

    `spec: dict`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`ConnectorResponse(**data: Any)`
:   Connector resource response model.
    
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

    `governance_metadata: dict | None`
    :   The type of the None singleton.

    `harness_managed: bool | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `spec: dict | None`
    :   The type of the None singleton.

    `status: dict | None`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`EnvironmentV2CreateRequest(**data: Any)`
:   EnvironmentV2 creation request model.
    
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

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`EnvironmentV2Response(**data: Any)`
:   EnvironmentV2 resource response model.
    
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

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`InfrastructureCreateRequest(**data: Any)`
:   Infrastructure creation request model.
    
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

    `allow_simultaneous_deployments: bool`
    :   The type of the None singleton.

    `deployment_type: str`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `environment_identifier: str`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `spec: dict`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`InfrastructureResponse(**data: Any)`
:   Infrastructure resource response model.
    
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

    `allow_simultaneous_deployments: bool`
    :   The type of the None singleton.

    `deployment_type: str`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `environment_identifier: str`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `spec: dict`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`OrganizationCreateRequest(**data: Any)`
:   Organization creation request model.
    
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

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`OrganizationResponse(**data: Any)`
:   Organization resource response model.
    
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

    `harness_managed: bool | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    ### Static methods

    `allow_null_string(v)`
    :   Validator for allow_null_string.
        
        Args:
            v: Parameter.
        
        Returns:
            Validated value.

`ProjectCreateRequest(**data: Any)`
:   Project creation request model.
    
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

    `color: str | None`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

`ProjectResponse(**data: Any)`
:   Project resource response model.
    
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

    `color: str | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `last_moved_at: int`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

    ### Static methods

    `allow_null_string(v)`
    :   Validator for allow_null_string.
        
        Args:
            v: Parameter.
        
        Returns:
            Validated value.

`SecretCreateRequest(**data: Any)`
:   Secret creation request model.
    
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

    `spec: dict`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`SecretResponse(**data: Any)`
:   Secret resource response model.
    
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

    `draft: bool | None`
    :   The type of the None singleton.

    `governance_metadata: dict | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `spec: dict`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

`ServiceCreateRequest(**data: Any)`
:   Service creation request model.
    
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

    `artifacts: dict | None`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `is_v2_service: bool`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

`ServiceOverrideCreateRequest(**data: Any)`
:   ServiceOverride creation request model (V2).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `application_settings: dict | None`
    :   The type of the None singleton.

    `config_files: list[dict] | None`
    :   The type of the None singleton.

    `connection_strings: dict | None`
    :   The type of the None singleton.

    `environment_ref: str | None`
    :   The type of the None singleton.

    `environment_variables: list[dict] | None`
    :   The type of the None singleton.

    `infra_identifier: str | None`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `org_identifier: str | None`
    :   The type of the None singleton.

    `override_type: str | None`
    :   The type of the None singleton.

    `project_identifier: str | None`
    :   The type of the None singleton.

    `service_ref: str | None`
    :   The type of the None singleton.

    `variables: list[dict] | None`
    :   The type of the None singleton.

`ServiceOverrideResponse(**data: Any)`
:   ServiceOverride resource response model (V2).
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `account_id: str | None`
    :   The type of the None singleton.

    `application_settings: dict | None`
    :   The type of the None singleton.

    `config_files: list[dict] | None`
    :   The type of the None singleton.

    `connection_strings: dict | None`
    :   The type of the None singleton.

    `environment_identifier: str | None`
    :   The type of the None singleton.

    `environment_variables: list[dict] | None`
    :   The type of the None singleton.

    `identifier: str | None`
    :   The type of the None singleton.

    `infra_identifier: str | None`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `org_identifier: str | None`
    :   The type of the None singleton.

    `override_type: str | None`
    :   The type of the None singleton.

    `project_identifier: str | None`
    :   The type of the None singleton.

    `service_identifier: str | None`
    :   The type of the None singleton.

    `variables: list[dict] | None`
    :   The type of the None singleton.

`ServiceResponse(**data: Any)`
:   Service resource response model.
    
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

    `artifacts: dict | None`
    :   The type of the None singleton.

    `created_at: int`
    :   The type of the None singleton.

    `description: str | None`
    :   The type of the None singleton.

    `identifier: str`
    :   The type of the None singleton.

    `is_v2_service: bool`
    :   The type of the None singleton.

    `manifests: list[dict] | None`
    :   The type of the None singleton.

    `name: str`
    :   The type of the None singleton.

    `org_identifier: str`
    :   The type of the None singleton.

    `project_identifier: str`
    :   The type of the None singleton.

    `store_type: str`
    :   The type of the None singleton.

    `tags: dict[str, str] | None`
    :   The type of the None singleton.

    `type: str`
    :   The type of the None singleton.

    `updated_at: int`
    :   The type of the None singleton.

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

`VariableCreateRequest(**data: Any)`
:   Variable creation request model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.ng_api.variables.VariableCore
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

`VariableResponse(**data: Any)`
:   Variable resource response model.
    
    Used for both get() and list() item responses.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.models.ng_api.variables.VariableCore
    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

`VariableSpec(**data: Any)`
:   Model for VariableSpec.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * harness_platform_sdk.base_model.HarnessModel
    * pydantic.main.BaseModel

    ### Class variables

    `fixed_value: str`
    :   The type of the None singleton.

    `type: str | None`
    :   The type of the None singleton.

    `value_type: str`
    :   The type of the None singleton.