Module harness_platform_sdk.pipeline_api.pipelines_v0
=====================================================
Pipelines API client for Harness SDK.

Provides CRUD operations for pipeline resources.

Classes
-------

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