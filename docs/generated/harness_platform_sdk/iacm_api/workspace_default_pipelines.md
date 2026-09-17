Module harness_platform_sdk.iacm_api.workspace_default_pipelines
================================================================
WorkspaceDefaultPipeline API client for Harness SDK.

Provides CRUD operations for workspacedefaultpipeliness resources.

Classes
-------

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