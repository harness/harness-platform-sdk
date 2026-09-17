Module harness_platform_sdk.iacm_api.workspace_variables
========================================================
WorkspaceVariables API client for Harness SDK.

Provides CRUD operations for workspacevariabless resources.

Classes
-------

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