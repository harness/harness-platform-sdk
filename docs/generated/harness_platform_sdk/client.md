Module harness_platform_sdk.client
==================================
Harness SDK client — main entry point for API interactions.

HarnessClient handles HTTP requests, scope resolution, URL construction,
error handling, and pagination. Supports both context manager and explicit close().

Classes
-------

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