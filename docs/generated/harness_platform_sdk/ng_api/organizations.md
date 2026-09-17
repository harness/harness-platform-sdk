Module harness_platform_sdk.ng_api.organizations
================================================
Organizations API client for Harness SDK.

Provides CRUD operations for organization resources.

Classes
-------

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