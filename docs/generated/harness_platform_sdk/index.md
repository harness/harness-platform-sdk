Module harness_platform_sdk
===========================
Harness Platform SDK.

A Python SDK for interacting with the Harness Platform API.
Provides unified access to all Harness APIs (Organizations, Projects,
Pipelines, Connectors, Secrets, and more) with built-in authentication,
scope management, pagination, and retry handling.

Sub-modules
-----------
* harness_platform_sdk.authz
* harness_platform_sdk.base_model
* harness_platform_sdk.client
* harness_platform_sdk.config
* harness_platform_sdk.exceptions
* harness_platform_sdk.iacm_api
* harness_platform_sdk.idp_api
* harness_platform_sdk.models
* harness_platform_sdk.ng_api
* harness_platform_sdk.pagination
* harness_platform_sdk.pipeline_api
* harness_platform_sdk.scope
* harness_platform_sdk.template_api

Classes
-------

`ApiError(status_code: int, body: str, headers: dict[str, str], payload: dict | None = None)`
:   Raised for non-2xx API responses (other than 401/403).
    
    Exposes HTTP status code, response body, and headers without revealing
    API keys or other secrets.
    
    Attributes:
        status_code: HTTP status code from API response.
        body: Response body as string.
        headers: Response headers dictionary.
        payload: Parsed JSON payload (if response was JSON), else None.
    
    Initialize ApiError.
    
    Args:
        status_code: HTTP status code from failed request.
        body: Raw response body as string.
        headers: Response headers as dictionary.
        payload: Parsed JSON payload from response (optional).

    ### Ancestors (in MRO)

    * harness_platform_sdk.exceptions.HarnessSdkError
    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * harness_platform_sdk.exceptions.AuthError

`AuthError(status_code: int, body: str, headers: dict[str, str], payload: dict | None = None)`
:   Raised for 401 (Unauthorized) and 403 (Forbidden) responses.
    
    Indicates authentication or authorization failure. Typically means
    the API key is missing, invalid, expired, or lacks required permissions.
    
    Initialize ApiError.
    
    Args:
        status_code: HTTP status code from failed request.
        body: Raw response body as string.
        headers: Response headers as dictionary.
        payload: Parsed JSON payload from response (optional).

    ### Ancestors (in MRO)

    * harness_platform_sdk.exceptions.ApiError
    * harness_platform_sdk.exceptions.HarnessSdkError
    * builtins.Exception
    * builtins.BaseException

`CatalogCustomPropertyApi(client: HarnessClient)`
:   API client for catalog_custom_properties operations.
    
    Initialize CatalogCustomPropertyApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for catalog custom property endpoints.
        
        Returns:
            str: The base API path for catalog custom property operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for catalog custom property data.
        
        Returns:
            str: The key used to extract catalog custom property data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for catalog custom property request bodies.
        
        Returns:
            str: The key used to wrap catalog custom property data in API requests, or None if not used.

    ### Methods

    `create(self, body: CatalogCustomPropertyCreateRequest, dry_run: bool | None = False, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse`
    :   Create a new catalog_custom_properties.
        
        Args:
            dry_run: Parameter.
            body: CatalogCustomPropertyCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            CatalogCustomPropertyResponse: The created catalog_custom_properties.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, body: CatalogCustomPropertyCreateRequest, dry_run: bool | None = False, scope: Scope | None = None) ‑> dict | None`
    :   Delete a catalog_custom_properties.
        
        Args:
            body: Parameter.
            dry_run: Parameter.
            identifier: catalog_custom_properties identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `generate_entity_ref(self, identifier: str, kind: str, **kwargs)`
    :   Process payload to create Entity Reference ID.

    `get_by_entity(self, identifier: str, kind: str, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponseByEntity`
    :   Get entities by custom_property in the specified organization.
        
        Args:
            identifier: Property identifier.
            kind: Entity kind.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            CatalogCustomPropertyResponse: Individual catalog_custom_properties items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `get_by_property(self, catalog_property: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse]`
    :   Get entities by custom_property in the specified organization.
        
        Args:
            catalog_property: String representation of the property to filter entities by.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            CatalogCustomPropertyResponse: Individual catalog_custom_properties items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, body: CatalogCustomPropertyCreateRequest, dry_run: bool | None = False, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse`
    :   Update an existing catalog_custom_properties.
        
        Args:
            body: CatalogCustomPropertyCreateRequest request with updated fields.
            dry_run: If True, perform a dry run without persisting changes.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            CatalogCustomPropertyResponse: The updated catalog_custom_properties.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

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

`EntityApi(client: HarnessClient)`
:   API client for entitiess operations.
    
    Initialize EntityApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for entity endpoints.
        
        Returns:
            str: The base API path for entity operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for entity data.
        
        Returns:
            str: The key used to extract entity data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for entity request bodies.
        
        Returns:
            str: The key used to wrap entity data in API requests, or None if not used.

    ### Methods

    `create(self, body: EntityCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Create a new entitiess.
        
        Args:
            body: EntityCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            EntityResponse: The created entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, kind: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a entitiess.
        
        Args:
            kind: Parameter.
            identifier: entitiess identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, kind: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Get a single entitiess by ID.
        
        Args:
            kind: Parameter.
            identifier: Entities identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EntityResponse: The requested entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, recursive=False, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.entities.EntityResponse]`
    :   List entitiesss in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            recursive: If True, recursively list entities.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            EntityResponse: Individual entitiess items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, kind: str, body: EntityCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Update an existing entitiess.
        
        Args:
            identifier: Parameter.
            kind: Parameter.
            identifier: entitiess identifier.
            body: EntityCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EntityResponse: The updated entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`HarnessClient(config: harness_platform_sdk.config.HarnessConfig | None = None, api_key: str | None = None, account_id: str | None = None, default_org: str | None = None, default_project: str | None = None, base_url: str | None = None)`
:   Main SDK client for interacting with Harness APIs.
    
    The client supports keyword argument construction for convenience:
        client = HarnessClient(api_key="...", account_id="...")
    
    Or via explicit config:
        config = HarnessConfig(api_key="...", account_id="...")
        client = HarnessClient(config=config)
    
    Supports both context manager and explicit close():
        with HarnessClient(...) as client:
            ...
    
        client = HarnessClient(...)
        try:
            ...
        finally:
            client.close()
    
    Initialize HarnessClient.
    
    Can be initialized with either explicit config or with keyword arguments.
    Supports both context manager and explicit close() for resource cleanup.
    
    Args:
        config: Explicit HarnessConfig. If provided, other kwargs are ignored.
        api_key: API key (used if config not provided).
        account_id: Account ID (used if config not provided).
        default_org: Default organization for scope resolution.
        default_project: Default project for scope resolution.
        base_url: Base URL for Harness API (used if config not provided).
    
    Raises:
        ValueError: If neither config nor (api_key, account_id) provided.
    
    Example:
        Initialize with keyword arguments::
    
            client = HarnessClient(
                api_key="your_api_key",
                account_id="your_account_id",
                default_org="my_organization"
            )
    
        Initialize with explicit config::
    
            from harness_platform_sdk import HarnessConfig
            config = HarnessConfig(
                api_key="your_api_key",
                account_id="your_account_id"
            )
            client = HarnessClient(config=config)
    
        Use as context manager::
    
            with HarnessClient(api_key="key", account_id="acct") as client:
                orgs = client.organizations.list_organizations()

    ### Instance variables

    `base_url: str`
    :   Get the base URL for the Harness API.
        
        Returns:
            Base URL string.

    `catalog_custom_properties`
    :   Lazy-loaded CatalogCustomPropertyApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> catalog_api = client.catalog_custom_properties
            >>> catalog_api is not None
            True

    `connectors`
    :   Lazy-loaded ConnectorsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> connectors_api = client.connectors
            >>> connectors_api is not None
            True

    `entities`
    :   Lazy-loaded EntityApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> entities_api = client.entities
            >>> entities_api is not None
            True

    `environments_v2`
    :   Lazy-loaded InfrastructureApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> environments_api = client.environments_v2
            >>> environments_api is not None
            True

    `infrastructures`
    :   Lazy-loaded InfrastructuresApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> infrastructures_api = client.infrastructures
            >>> infrastructures_api is not None
            True

    `input_sets_v0`
    :   Lazy-loaded InputSetsV0Api instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> input_sets_api = client.input_sets_v0
            >>> input_sets_api is not None
            True

    `organizations`
    :   Lazy-loaded OrganizationsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient, Scope
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> org_api = client.organizations
            >>> org_api is not None
            True

    `pipelines_v0`
    :   Lazy-loaded PipelinesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> pipelines_api = client.pipelines_v0
            >>> pipelines_api is not None
            True

    `projects`
    :   Lazy-loaded ProjectsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> projects_api = client.projects
            >>> projects_api is not None
            True

    `resource_groups`
    :   Lazy-loaded ResourceGroupsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> resource_groups_api = client.resource_groups
            >>> resource_groups_api is not None
            True

    `role_assignments`
    :   Lazy-loaded RoleAssignmentsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> role_assignments_api = client.role_assignments
            >>> role_assignments_api is not None
            True

    `roles`
    :   Lazy-loaded RolesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> roles_api = client.roles
            >>> roles_api is not None
            True

    `scores`
    :   Lazy-loaded ScoreApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> scores_api = client.scores
            >>> scores_api is not None
            True

    `secrets`
    :   Lazy-loaded SecretsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> secrets_api = client.secrets
            >>> secrets_api is not None
            True

    `service_overrides`
    :   Lazy-loaded ServiceOverridesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> service_overrides_api = client.service_overrides
            >>> service_overrides_api is not None
            True

    `services`
    :   Lazy-loaded ServicesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> services_api = client.services
            >>> services_api is not None
            True

    `templates_v0`
    :   Lazy-loaded TemplatesV0Api instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> templates_api = client.templates_v0
            >>> templates_api is not None
            True

    `triggers_v0`
    :   Lazy-loaded TriggersV0Api instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> triggers_api = client.triggers_v0
            >>> triggers_api is not None
            True

    `user_groups`
    :   Lazy-loaded UserGroupsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> user_groups_api = client.user_groups
            >>> user_groups_api is not None
            True

    `variables`
    :   Lazy-loaded VariablesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> variables_api = client.variables
            >>> variables_api is not None
            True

    `workspace_approvals`
    :   Lazy-loaded WorkspaceApprovalsApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_approvals_api = client.workspace_approvals
            >>> workspace_approvals_api is not None
            True

    `workspace_default_pipelines`
    :   Lazy-loaded WorkspaceDefaultPipelinesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_default_pipelines_api = client.workspace_default_pipelines
            >>> workspace_default_pipelines_api is not None
            True

    `workspace_states`
    :   Lazy-loaded WorkspaceStatesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_states_api = client.workspace_states
            >>> workspace_states_api is not None
            True

    `workspace_variables`
    :   Lazy-loaded WorkspaceVariablesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_variables_api = client.workspace_variables
            >>> workspace_variables_api is not None
            True

    `workspaces`
    :   Lazy-loaded WorkspacesApi instance.
        
        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspaces_api = client.workspaces
            >>> workspaces_api is not None
            True

    ### Methods

    `close(self) ‑> None`
    :   Close the underlying HTTP client.
        
        Closes the httpx.Client and releases any open connections.

    `set_default_scope(self, org: str | None = None, project: str | None = None) ‑> None`
    :   Update the default scope for requests.
        
        Args:
            org: New default organization.
            project: New default project.
        
        Raises:
            Exception: If project is set without org.

`HarnessConfig(**data: Any)`
:   Configuration for HarnessClient.
    
    Attributes:
        api_key: Harness API key for authentication.
        account_id: Harness account identifier.
        base_url: Base URL for Harness API (default: https://app.harness.io).
        timeout: Request timeout in seconds (default: 30.0).
        max_retries: Maximum number of connection retries (default: 3).
        retry_status_codes: HTTP status codes to retry on (default: [429, 503]).
        retry_enabled: Whether to retry failed requests (default: True).
        verify_ssl: Whether to verify SSL certificates (default: True).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `account_id: str`
    :   The type of the None singleton.

    `api_key: str`
    :   The type of the None singleton.

    `base_url: str`
    :   The type of the None singleton.

    `max_retries: int`
    :   The type of the None singleton.

    `model_config`
    :   The type of the None singleton.

    `retry_enabled: bool`
    :   The type of the None singleton.

    `retry_status_codes: list[int]`
    :   The type of the None singleton.

    `timeout: float`
    :   The type of the None singleton.

    `verify_ssl: bool`
    :   The type of the None singleton.

    ### Methods

    `merge_duplicates(self, items, key='name')`
    :   Merge duplicate items by key, combining values.

`HarnessSdkError(*args, **kwargs)`
:   Base exception for all Harness SDK errors.
    
    All SDK exceptions inherit from this class, allowing callers to catch
    any Harness-specific error with a single except clause.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * harness_platform_sdk.exceptions.ApiError
    * harness_platform_sdk.exceptions.ScopeNotSetError

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

`InputSetsV0Api(client: HarnessClient)`
:   API client for inputset operations.
    
    Initialize InputsetsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for input set endpoints.
        
        Returns:
            str: The base API path for input set operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for input set data.
        
        Returns:
            str: The key used to extract input set data from API responses.

    `wrap_key: str`
    :   Get the wrap key for input set request bodies.
        
        Returns:
            str: The key used to wrap input set data in API requests.

    ### Methods

    `create(self, body: InputSetV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0Response`
    :   Create a new inputset.
        
        Args:
            body: InputSetV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            InputSetV0Response: The created inputset.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a inputset.
        
        Args:
            pipeline_identifier: Parameter specification.
            identifier: inputset identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0Response`
    :   Get a single inputset by ID.
        
        Args:
            pipeline_identifier: Parameter specification.
            identifier: Inputset identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            InputSetV0Response: The requested inputset.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, pipeline_identifier: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0ListResponse]`
    :   List inputsets in the specified organization.
        
        Args:
            pipeline_identifier: Parameter specification.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            InputSetV0Response: Individual inputset items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: InputSetV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.input_sets_v0.InputSetV0Response`
    :   Update an existing inputset.
        
        Args:
            identifier: inputset identifier.
            body: InputSetV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            InputSetV0Response: The updated inputset.
        
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

`PipelinesV0Api(client: HarnessClient)`
:   API client for pipeline operations.
    
    Initialize PipelinesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for pipeline endpoints.
        
        Returns:
            str: The base API path for pipeline operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for pipeline data.
        
        Returns:
            str: The key used to extract pipeline data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for pipeline request bodies.
        
        Returns:
            str: The key used to wrap pipeline data in API requests.

    ### Methods

    `create(self, body: PipelineV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0Response`
    :   Create a new pipeline.
        
        Args:
            body: PipelineV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            PipelineV0Response: The created pipeline.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a pipeline.
        
        Args:
            identifier: pipeline identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0Response`
    :   Get a single pipeline by ID.
        
        Args:
            identifier: Pipeline identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            PipelineV0Response: The requested pipeline.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0Response]`
    :   List pipelines in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            PipelineV0Response: Individual pipeline items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: PipelineV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.pipelines_v0.PipelineV0Response`
    :   Update an existing pipeline.
        
        Args:
            identifier: pipeline identifier.
            body: PipelineV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            PipelineV0Response: The updated pipeline.
        
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

`ResourceGroupsApi(client: HarnessClient)`
:   API client for resource_group operations.
    
    Initialize ResourceGroupsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for resource group endpoints.
        
        Returns:
            str: The base API path for resource group operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for resource group data.
        
        Returns:
            str: The key used to extract resource group data from API responses.

    ### Methods

    `create(self, body: ResourceGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse`
    :   Create a new resource_group.
        
        Args:
            body: ResourceGroupCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ResourceGroupResponse: The created resource_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a resource_group.
        
        Args:
            identifier: resource_group identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse`
    :   Get a single resource_group by ID.
        
        Args:
            identifier: ResourceGroup identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ResourceGroupResponse: The requested resource_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse]`
    :   List resource_groups in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ResourceGroupResponse: Individual resource_group items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ResourceGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse`
    :   Update an existing resource_group.
        
        Args:
            identifier: resource_group identifier.
            body: ResourceGroupCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ResourceGroupResponse: The updated resource_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`RoleAssignmentsApi(client: HarnessClient)`
:   API client for role_assignment operations.
    
    Initialize RoleAssignmentsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for role assignment endpoints.
        
        Returns:
            str: The base API path for role assignment operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as role assignment request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for role assignment data.
        
        Returns:
            str: The key used to extract role assignment data from API responses.

    ### Methods

    `create(self, body: RoleAssignmentCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse`
    :   Create a new role_assignment.
        
        Args:
            body: RoleAssignmentCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            RoleAssignmentResponse: The created role_assignment.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a role_assignment.
        
        Args:
            identifier: role_assignment identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse`
    :   Get a single role_assignment by ID.
        
        Args:
            identifier: RoleAssignment identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleAssignmentResponse: The requested role_assignment.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse]`
    :   List role_assignments in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            RoleAssignmentResponse: Individual role_assignment items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: RoleAssignmentCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse`
    :   Update an existing role_assignment.
        
        Args:
            identifier: role_assignment identifier.
            body: RoleAssignmentCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleAssignmentResponse: The updated role_assignment.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`RolesApi(client: HarnessClient)`
:   API client for role operations.
    
    Initialize RolesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for role endpoints.
        
        Returns:
            str: The base API path for role operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for role data.
        
        Returns:
            str: The key used to extract role data from API responses.

    ### Methods

    `create(self, body: RoleCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.roles.RoleResponse`
    :   Create a new role.
        
        Args:
            body: RoleCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            RoleResponse: The created role.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a role.
        
        Args:
            identifier: role identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.roles.RoleResponse`
    :   Get a single role by ID.
        
        Args:
            identifier: Role identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleResponse: The requested role.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.authz.roles.RoleResponse]`
    :   List roles in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            RoleResponse: Individual role items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: RoleCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.roles.RoleResponse`
    :   Update an existing role.
        
        Args:
            identifier: role identifier.
            body: RoleCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleResponse: The updated role.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`Scope(**data: Any)`
:   Represents the account/org/project scope for API requests.
    
    The scope is frozen — once created, it cannot be modified.
    The account_id is required; org and project are optional.
    
    Attributes:
        account_id: Harness account identifier (required).
        org: Harness organization identifier (optional).
        project: Harness project identifier (optional).
        pipeline: Harness pipeline identifier (optional).
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `account_id: str`
    :   The type of the None singleton.

    `model_config`
    :   The type of the None singleton.

    `org: str | None`
    :   The type of the None singleton.

    `pipeline: str | None`
    :   The type of the None singleton.

    `project: str | None`
    :   The type of the None singleton.

`ScopeNotSetError(*args, **kwargs)`
:   Raised when required scope fields are not set or provided.
    
    Indicates that required scope fields (account_id, org, project, etc.)
    are missing and cannot be resolved from defaults.

    ### Ancestors (in MRO)

    * harness_platform_sdk.exceptions.HarnessSdkError
    * builtins.Exception
    * builtins.BaseException

`ScoreApi(client: HarnessClient)`
:   API client for scores operations.
    
    Initialize ScoreApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for score endpoints.
        
        Returns:
            str: The base API path for score operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for score data.
        
        Returns:
            str: The key used to extract score data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for score request bodies.
        
        Returns:
            str: The key used to wrap score data in API requests, or None if not used.

    ### Methods

    `get(self, identifier: str, kind: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.scores.ScoreResponse]`
    :   Get a single scores by Entity Identifier and Kind.
        
        Args:
            identifier: Entity identifier.
            kind: Entity kind.
            scope: Entity Scope . If None, uses client default scope.
            **kwargs: Additional query parameters.
        
        Yields:
            ScoreResponse: The requested scores.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `get_summary(self, identifier: str, kind: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.scores.ScoreSummaryResponse`
    :   Get a summary of scores by Entity Identifier and Kind.
        
        Args:
            identifier: Entity identifier.
            kind: Entity kind.
            scope: Entity Scope . If None, uses client default scope.
        
        Returns:
            ScoreResponse: The requested scores.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, kind: str, entity_type: str | None = None, owners: list[str] | None = None, tags: list[str] | None = None, lifecycle: list[str] | None = None, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.scores.ScoreResponse`
    :   List scores by kind and filters.
        
        Args:
            kind: Entity kind.
            entity_type: Entity entity_type.
            owners: List of Entity owners.
            tags: List of Entity tags.
            lifecycle: List of Entity lifecycle.
            scope: Entity Scope . If None, uses client default scope.
        
        Yields:
            ScoreResponse: Individual scores items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `recalibrate(self, identifier: str, kind: str, scorecard_identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.scores.ScoreSummaryResponse`
    :   API for Recalibrating the score for scorecard of entity.
        
        Args:
            body: Request body.
            dry_run: If True, perform a dry run without persisting changes.
            identifier: Entity identifier.
            kind: Entity kind.
            scorecard_identifier: Scorecard Identifer.
            scope: Entity Scope . If None, uses client default scope.
        
        Returns:
            ScoreResponse: The requested scores.
        
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

`TemplatesV0Api(client: HarnessClient)`
:   API client for templates_v0 operations.
    
    Initialize TemplatesV0Api with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for template endpoints.
        
        Returns:
            str: The base API path for template operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for template data.
        
        Returns:
            str: The key used to extract template data from API responses.

    `wrap_key: str`
    :   Get the wrap key for template request bodies.
        
        Returns:
            str: The key used to wrap template data in API requests.

    ### Methods

    `apply_templates(self, original_entity_yaml: str, scope: Scope | None = None, check_for_access: bool | None = None, get_merged_yaml_with_template_field: bool | None = None, get_only_file_content: bool | None = None, yaml_version: str | None = None, enforce_opa_on_execution: bool | None = None, **kwargs) ‑> dict`
    :   Get complete YAML with template references resolved.
        
        Applies template references in the provided YAML and returns the complete
        resolved YAML with all template references substituted.
        
        Args:
            original_entity_yaml: The YAML content with template references.
            scope: Scope containing resource scope. If None, uses client default scope.
            check_for_access: Whether to check access for referenced templates.
            get_merged_yaml_with_template_field: Include merged YAML with template field.
            get_only_file_content: Return only file content without metadata.
            yaml_version: Harness YAML version to use.
            enforce_opa_on_execution: Enforce OPA policies on execution.
            **kwargs: Additional query parameters (e.g., branch, repoIdentifier).
        
        Returns:
            dict: Response containing resolved YAML and metadata.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `create(self, body: TemplateV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Create a new templates_v0.
        
        Args:
            body: TemplateV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            TemplateV0Response: The created templates_v0.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, version_label: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a templates_v0.
        
        Args:
            version_label: Parameter specification.
            identifier: templates_v0 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Get a single templates_v0 by ID.
        
        Args:
            identifier: TemplateV0 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TemplateV0Response: The requested templates_v0.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get_entity_usage(self, identifier: str, scope: Scope | None = None, page_index: int | None = None, page_size: int | None = None, **kwargs) ‑> dict`
    :   Get entities (pipelines, stages) that reference a template.
        
        Args:
            identifier: Template identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            page_index: Page index for pagination.
            page_size: Page size for pagination.
            **kwargs: Additional query parameters (e.g., searchTerm, versionLabel).
        
        Returns:
            dict: Paginated response with entity usage data.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get_labels(self, identifier: str, scope: Scope | None = None, **kwargs) ‑> dict`
    :   Get custom labels for template versions.
        
        Args:
            identifier: Template identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., versionLabel).
        
        Returns:
            dict: Map of version labels to custom labels.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, template_type: str | None = 'All', scope: Scope | None = None, **kwargs) ‑> Iterator[TemplateV0ListResponse]`
    :   List templates_v0s in the specified organization.
        
        Args:
            template_type: Parameter specification.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            TemplateV0ListResponse: Individual templates_v0 items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `refresh_and_get(self, identifier: str, branch: str, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Refresh cache and fetch a template from remote git source.
        
        Force-refreshes the git file cache for a remote Template and returns the
        freshly fetched entity.
        
        Args:
            identifier: Template identifier.
            branch: Git branch name (required).
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., versionLabel, label).
        
        Returns:
            TemplateV0Response: The refreshed template.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `resolve_template(self, identifier: str, version: str, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Get complete YAML with template references resolved.
        
        Applies template references in the provided YAML and returns the complete
        resolved YAML with all template references substituted.
        
        Args:
            identifier: TemplateV0 identifier.
            version: TemplateV0 version.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., getDefaultFromOtherRepo, loadFromFallbackBranch).
        
        Returns:
            TemplateV0Response: The requested templates_v0 merged with references.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `update(self, identifier: str, body: TemplateV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Update an existing templates_v0.
        
        Args:
            identifier: templates_v0 identifier.
            body: TemplateV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TemplateV0Response: The updated templates_v0.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`TriggersV0Api(client: HarnessClient)`
:   API client for trigger operations.
    
    Initialize TriggersApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for trigger endpoints.
        
        Returns:
            str: The base API path for trigger operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for trigger data.
        
        Returns:
            str: The key used to extract trigger data from API responses.

    `wrap_key: str`
    :   Get the wrap key for trigger request bodies.
        
        Returns:
            str: The key used to wrap trigger data in API requests.

    ### Methods

    `create(self, body: TriggerV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response`
    :   Create a new trigger.
        
        Args:
            body: TriggerV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            TriggerV0Response: The created trigger.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a trigger.
        
        Args:
            pipeline_identifier: Parameter specification.
            identifier: trigger identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response`
    :   Get a single trigger by ID.
        
        Args:
            pipeline_identifier: Parameter specification.
            identifier: Trigger identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TriggerV0Response: The requested trigger.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, pipeline_identifier: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response]`
    :   List triggers in the specified organization.
        
        Args:
            pipeline_identifier: Parameter specification.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            TriggerV0Response: Individual trigger items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: TriggerV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response`
    :   Update an existing trigger.
        
        Args:
            identifier: trigger identifier.
            body: TriggerV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TriggerV0Response: The updated trigger.
        
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

`WorkspaceApprovalsApi(client: HarnessClient)`
:   API client for workspaceapprovals operations.
    
    Initialize WorkspaceApprovalsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace approval endpoints.
        
        Returns:
            str: The base API path for workspace approval operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace approval request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace approval data.
        
        Returns:
            str: The key used to extract workspace approval data from API responses, or None if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace approval request bodies.
        
        Returns:
            str: The key used to wrap workspace approval data in API requests, or None if not used.

    ### Methods

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspaceapprovals.
        
        Args:
            identifier: workspaceapprovals identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalResponse`
    :   Get a single workspaceapprovals by ID.
        
        Args:
            identifier: WorkspaceApproval identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceApprovalResponse: The requested workspaceapprovals.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, workspace_identifier: str, status: WorkspaceApprovalStatus | None = None, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalListResponse]`
    :   List workspaceapprovalss in the specified organization.
        
        Args:
            status: Parameter.
            workspace_identifier: Parameter.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceApprovalResponse: Individual workspaceapprovals items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: WorkspaceApprovalCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalResponse`
    :   Update an existing workspaceapprovals.
        
        Args:
            identifier: workspaceapprovals identifier.
            body: WorkspaceApprovalCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceApprovalResponse: The updated workspaceapprovals.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspaceDefaultPipelinesApi(client: HarnessClient)`
:   API client for workspacedefaultpipeliness operations.
    
    Initialize WorkspaceDefaultPipelineApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace default pipeline endpoints.
        
        Returns:
            str: The base API path for workspace default pipeline operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace default pipeline request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace default pipeline data.
        
        Returns:
            str: The key used to extract workspace default pipeline data from API responses, or None if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace default pipeline request bodies.
        
        Returns:
            str: The key used to wrap workspace default pipeline data in API requests, or None if not used.

    ### Methods

    `delete(self, body: WorkspaceDefaultPipelineCreateRequest, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspacedefaultpipeliness.
        
        Args:
            body: Request body.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, workspace_identifier: str | None = None, operation: WorkspaceDefaultPipelineOperation | None = None, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse`
    :   Get a single workspacedefaultpipeliness by ID.
        
        Args:
            operation: Parameter.
            workspace_identifier: Workspacedefaultpipelines workspace_identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceDefaultPipelineResponse: The requested workspacedefaultpipeliness.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse]`
    :   List workspacedefaultpipelinesss in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceDefaultPipelineResponse: Individual workspacedefaultpipeliness items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, body: WorkspaceDefaultPipelineCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse`
    :   Update an existing workspacedefaultpipeliness.
        
        Args:
            identifier: workspacedefaultpipeliness identifier.
            body: WorkspaceDefaultPipelineCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceDefaultPipelineResponse: The updated workspacedefaultpipeliness.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspaceStatesApi(client: HarnessClient)`
:   API client for workspacestates operations.
    
    Initialize WorkspacestatesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace state endpoints.
        
        Returns:
            str: The base API path for workspace state operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace state request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace state data.
        
        Returns:
            str: The key used to extract workspace state data from API responses, or None if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace state request bodies.
        
        Returns:
            str: The key used to wrap workspace state data in API requests, or None if not used.

    ### Methods

    `create(self, identifier: str, body: WorkspaceStateCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_states.WorkspaceStateResponse`
    :   Create a new workspacestates.
        
        Args:
            identifier: Workspace state identifier.
            body: WorkspaceStateCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceStateResponse: The created workspacestates.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_states.WorkspaceStateResponse`
    :   Get a single workspacestates by ID.
        
        Args:
            identifier: Workspacestate identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceStateResponse: The requested workspacestates.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspaceVariablesApi(client: HarnessClient)`
:   API client for workspacevariabless operations.
    
    Initialize WorkspaceVariablesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace variable endpoints.
        
        Returns:
            str: The base API path for workspace variable operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace variable data.
        
        Returns:
            str: The key used to extract workspace variable data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for workspace variable request bodies.
        
        Returns:
            str: The key used to wrap workspace variable data in API requests, or None if not used.

    ### Methods

    `create(self, body: WorkspaceVariableCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse`
    :   Create a new workspacevariabless.
        
        Args:
            body: WorkspaceVariableCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            WorkspaceVariableResponse: The created workspacevariabless.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, workspace_identifier: str, kind: WorkspaceVariableKind, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspacevariabless.
        
        Args:
            kind: Parameter.
            workspace_identifier: Parameter.
            identifier: workspacevariabless identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, workspace_identifier: str, kind: WorkspaceVariableKind, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse`
    :   Get a single workspacevariabless by ID.
        
        Args:
            kind: Parameter.
            workspace_identifier: Parameter.
            identifier: Workspacevariables identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceVariableResponse: The requested workspacevariabless.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, workspace_identifier: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse]`
    :   List workspacevariablesss in the specified organization.
        
        Args:
            workspace_identifier: Parameter.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceVariableResponse: Individual workspacevariabless items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: WorkspaceVariableCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse`
    :   Update an existing workspacevariabless.
        
        Args:
            identifier: workspacevariabless identifier.
            body: WorkspaceVariableCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceVariableResponse: The updated workspacevariabless.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspacesApi(client: HarnessClient)`
:   API client for workspaces operations.
    
    Initialize WorkspacesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace endpoints.
        
        Returns:
            str: The base API path for workspace operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace data.
        
        Returns:
            str: The key used to extract workspace data from API responses, or "none" if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace request bodies.
        
        Returns:
            str: The key used to wrap workspace data in API requests, or "none" if not used.

    ### Methods

    `create(self, body: WorkspaceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse`
    :   Create a new workspaces.
        
        Args:
            body: WorkspaceCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            WorkspaceResponse: The created workspaces.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspaces.
        
        Args:
            identifier: workspaces identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse`
    :   Get a single workspaces by ID.
        
        Args:
            identifier: Workspace identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceResponse: The requested workspaces.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse]`
    :   List workspacess in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceResponse: Individual workspaces items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: WorkspaceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse`
    :   Update an existing workspaces.
        
        Args:
            identifier: workspaces identifier.
            body: WorkspaceCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceResponse: The updated workspaces.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.