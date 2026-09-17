Module harness_platform_sdk.iacm_api.workspaces
===============================================
Workspaces API client for Harness SDK.

Provides CRUD operations for workspaces resources.

Classes
-------

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