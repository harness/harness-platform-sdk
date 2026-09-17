Module harness_platform_sdk.iacm_api.workspace_states
=====================================================
Workspacestates API client for Harness SDK.

Provides CRUD operations for workspacestates resources.

Classes
-------

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