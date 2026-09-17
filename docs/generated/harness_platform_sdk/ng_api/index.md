Module harness_platform_sdk.ng_api
==================================
Next Generation API resources.

Provides APIs for managing organizations, projects, connectors, secrets,
services, user groups, and other resources under the /ng/ path root.

Sub-modules
-----------
* harness_platform_sdk.ng_api.connectors
* harness_platform_sdk.ng_api.environments_v2
* harness_platform_sdk.ng_api.infrastructures
* harness_platform_sdk.ng_api.organizations
* harness_platform_sdk.ng_api.projects
* harness_platform_sdk.ng_api.secrets
* harness_platform_sdk.ng_api.service_overrides
* harness_platform_sdk.ng_api.services
* harness_platform_sdk.ng_api.user_groups
* harness_platform_sdk.ng_api.variables

Classes
-------

`ConnectorsApi(client: HarnessClient)`
:   API client for connector operations.
    
    Initialize ConnectorsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for connector endpoints.
        
        Returns:
            str: The base API path for connector operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for connector data.
        
        Returns:
            str: The key used to extract connector data from API responses.

    ### Methods

    `create(self, body: ConnectorCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.connectors.ConnectorResponse`
    :   Create a new connector.
        
        Args:
            body: ConnectorCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ConnectorResponse: The created connector.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a connector.
        
        Args:
            identifier: connector identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.connectors.ConnectorResponse`
    :   Get a single connector by ID.
        
        Args:
            identifier: Connector identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ConnectorResponse: The requested connector.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.connectors.ConnectorResponse]`
    :   List connectors in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ConnectorResponse: Individual connector items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ConnectorCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.connectors.ConnectorResponse`
    :   Update an existing connector.
        
        Args:
            identifier: connector identifier.
            body: ConnectorCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ConnectorResponse: The updated connector.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`EnvironmentsV2Api(client: HarnessClient)`
:   API client for environments_v2 operations.
    
    Initialize EnvironmentsV2Api with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for environment endpoints.
        
        Returns:
            str: The base API path for environment operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for environment data.
        
        Returns:
            str: The key used to extract environment data from API responses.

    `wrap_key: str`
    :   Get the wrap key for environment request bodies.
        
        Returns:
            str: The key used to wrap environment data in API requests, or None if no wrapping.

    ### Methods

    `create(self, body: EnvironmentV2CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response`
    :   Create a new environments_v2.
        
        Args:
            body: EnvironmentV2CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            EnvironmentV2Response: The created environments_v2.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a environments_v2.
        
        Args:
            identifier: environments_v2 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response`
    :   Get a single environments_v2 by ID.
        
        Args:
            identifier: EnvironmentV2 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EnvironmentV2Response: The requested environments_v2.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response]`
    :   List environments_v2s in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            EnvironmentV2Response: Individual environments_v2 items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: EnvironmentV2CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response`
    :   Update an existing environments_v2.
        
        Args:
            identifier: environments_v2 identifier.
            body: EnvironmentV2CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EnvironmentV2Response: The updated environments_v2.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`InfrastructuresApi(client: HarnessClient)`
:   API client for infrastructures operations.
    
    Initialize InfrastructuresApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for infrastructure endpoints.
        
        Returns:
            str: The base API path for infrastructure operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for infrastructure data.
        
        Returns:
            str: The key used to extract infrastructure data from API responses.

    `wrap_key: str`
    :   Get the wrap key for infrastructure request bodies.
        
        Returns:
            str: The key used to wrap infrastructure data in API requests.

    ### Methods

    `create(self, body: InfrastructureCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.infrastructures.InfrastructureResponse`
    :   Create a new infrastructures.
        
        Args:
            body: InfrastructureCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            InfrastructureResponse: The created infrastructures.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, environment_identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a infrastructures.
        
        Args:
            environment_identifier: Parameter specification.
            identifier: infrastructures identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, environment_identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.infrastructures.InfrastructureResponse`
    :   Get a single infrastructures by ID.
        
        Args:
            environment_identifier: Parameter specification.
            identifier: Infrastructure identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            InfrastructureResponse: The requested infrastructures.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, environment_identifier: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.infrastructures.InfrastructureResponse]`
    :   List infrastructuress in the specified organization.
        
        Args:
            environment_identifier: Parameter specification.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            InfrastructureResponse: Individual infrastructures items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: InfrastructureCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.infrastructures.InfrastructureResponse`
    :   Update an existing infrastructures.
        
        Args:
            identifier: infrastructures identifier.
            body: InfrastructureCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            InfrastructureResponse: The updated infrastructures.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`OrganizationsApi(client: HarnessClient)`
:   API client for organization operations.
    
    Initialize OrganizationsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for organization endpoints.
        
        Returns:
            str: The base API path for organization operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for organization data.
        
        Returns:
            str: The key used to extract organization data from API responses.

    ### Methods

    `create(self, body: OrganizationCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.organizations.OrganizationResponse`
    :   Create a new organization.
        
        Args:
            body: OrganizationCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            OrganizationResponse: The created organization.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a organization.
        
        Args:
            identifier: organization identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.organizations.OrganizationResponse`
    :   Get a single organization by ID.
        
        Args:
            identifier: Organization identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            OrganizationResponse: The requested organization.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.organizations.OrganizationResponse]`
    :   List organizations in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            OrganizationResponse: Individual organization items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: OrganizationCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.organizations.OrganizationResponse`
    :   Update an existing organization.
        
        Args:
            identifier: organization identifier.
            body: OrganizationCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            OrganizationResponse: The updated organization.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`ProjectsApi(client: HarnessClient)`
:   API client for project operations.
    
    Initialize ProjectsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for project endpoints.
        
        Returns:
            str: The base API path for project operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for project data.
        
        Returns:
            str: The key used to extract project data from API responses.

    ### Methods

    `create(self, body: ProjectCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.projects.ProjectResponse`
    :   Create a new project.
        
        Args:
            body: ProjectCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ProjectResponse: The created project.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a project.
        
        Args:
            identifier: project identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.projects.ProjectResponse`
    :   Get a single project by ID.
        
        Args:
            identifier: Project identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ProjectResponse: The requested project.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.projects.ProjectResponse]`
    :   List projects in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ProjectResponse: Individual project items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ProjectCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.projects.ProjectResponse`
    :   Update an existing project.
        
        Args:
            identifier: project identifier.
            body: ProjectCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ProjectResponse: The updated project.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`SecretsApi(client: HarnessClient)`
:   API client for secret operations.
    
    Initialize SecretsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for secret endpoints.
        
        Returns:
            str: The base API path for secret operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for secret data.
        
        Returns:
            str: The key used to extract secret data from API responses.

    ### Methods

    `create(self, body: SecretCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.secrets.SecretResponse`
    :   Create a new secret.
        
        Args:
            body: SecretCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            SecretResponse: The created secret.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a secret.
        
        Args:
            identifier: secret identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.secrets.SecretResponse`
    :   Get a single secret by ID.
        
        Args:
            identifier: Secret identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            SecretResponse: The requested secret.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.secrets.SecretResponse]`
    :   List secrets in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            SecretResponse: Individual secret items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: SecretCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.secrets.SecretResponse`
    :   Update an existing secret.
        
        Args:
            identifier: secret identifier.
            body: SecretCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            SecretResponse: The updated secret.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`ServiceOverridesApi(client: HarnessClient)`
:   API client for service_overrides operations.
    
    Initialize ServiceOverridesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for service overrides.

    `should_wrap: bool`
    :   Check if response should be wrapped (False for service overrides).

    `unwrap_key: str`
    :   Get the unwrap key (None for service overrides).

    `wrap_key: str`
    :   Get the wrap key (None for service overrides).

    ### Methods

    `create(self, body: ServiceOverrideCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse`
    :   Create a new service_overrides.
        
        Args:
            body: ServiceOverrideCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ServiceOverrideResponse: The created service_overrides.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None, **kwargs) ‑> dict | None`
    :   Delete a service override.
        
        Args:
            identifier: Service override identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, environment_identifier: str, service_identifier: str | None = None, infra_identifier: str | None = None, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse`
    :   Get a single service_overrides by ID.
        
        Args:
            environment_identifier: Environment identifier.
            service_identifier: Service identifier (optional).
            infra_identifier: Infrastructure identifier (optional).
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters.
        
        Returns:
            ServiceOverrideResponse: The requested service_overrides.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, override_type: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse]`
    :   List service overrides for an environment.
        
        Args:
            scope: Scope containing account/org/project. If None, uses client default scope.
            override_type: Override Type identifier (e.g. ENV_GLOBAL_OVERRIDE. Required for list).
            **kwargs: Additional query parameters.
        
        Yields:
            ServiceOverrideResponse: Individual service override items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ServiceOverrideCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse`
    :   Update an existing service_overrides.
        
        Args:
            identifier: service_overrides identifier.
            body: ServiceOverrideCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ServiceOverrideResponse: The updated service_overrides.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`ServicesApi(client: HarnessClient)`
:   API client for service operations.
    
    Initialize ServicesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for service endpoints.
        
        Returns:
            str: The base API path for service operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for service data.
        
        Returns:
            str: The key used to extract service data from API responses.

    `wrap_key: str`
    :   Get the wrap key for service request bodies.
        
        Returns:
            str: The key used to wrap service data in API requests.

    ### Methods

    `create(self, body: ServiceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.services.ServiceResponse`
    :   Create a new service.
        
        Args:
            body: ServiceCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ServiceResponse: The created service.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a service.
        
        Args:
            identifier: service identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.services.ServiceResponse`
    :   Get a single service by ID.
        
        Args:
            identifier: Service identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ServiceResponse: The requested service.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.services.ServiceResponse]`
    :   List services in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ServiceResponse: Individual service items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ServiceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.services.ServiceResponse`
    :   Update an existing service.
        
        Args:
            identifier: service identifier.
            body: ServiceCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ServiceResponse: The updated service.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`UserGroupsApi(client: HarnessClient)`
:   API client for user_group operations.
    
    Initialize UserGroupsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for user group endpoints.
        
        Returns:
            str: The base API path for user group operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as user group request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for user group data.
        
        Returns:
            str: The key used to extract user group data from API responses, or None if no unwrapping needed.

    ### Methods

    `create(self, body: UserGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse`
    :   Create a new user_group.
        
        Args:
            body: UserGroupCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            UserGroupResponse: The created user_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a user_group.
        
        Args:
            identifier: user_group identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse`
    :   Get a single user_group by ID.
        
        Args:
            identifier: UserGroup identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            UserGroupResponse: The requested user_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse]`
    :   List user_groups in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            UserGroupResponse: Individual user_group items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: UserGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse`
    :   Update an existing user_group.
        
        Args:
            identifier: user_group identifier.
            body: UserGroupCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            UserGroupResponse: The updated user_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`VariablesApi(client: HarnessClient)`
:   API client for variables operations.
    
    Initialize VariablesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for variable endpoints.
        
        Returns:
            str: The base API path for variable operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for variable data.
        
        Returns:
            str: The key used to extract variable data from API responses.

    `wrap_key: str`
    :   Get the wrap key for variable request bodies.
        
        Returns:
            str: The key used to wrap variable data in API requests.

    ### Methods

    `create(self, body: VariableCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.variables.VariableResponse`
    :   Create a new variables.
        
        Args:
            body: VariableCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            VariableResponse: The created variables.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a variables.
        
        Args:
            identifier: variables identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.variables.VariableResponse`
    :   Get a single variables by ID.
        
        Args:
            identifier: Variable identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            VariableResponse: The requested variables.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.variables.VariableResponse]`
    :   List variabless in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            VariableResponse: Individual variables items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: VariableCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.variables.VariableResponse`
    :   Update an existing variables.
        
        Args:
            identifier: variables identifier.
            body: VariableCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            VariableResponse: The updated variables.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.