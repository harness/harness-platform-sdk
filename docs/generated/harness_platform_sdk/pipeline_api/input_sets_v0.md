Module harness_platform_sdk.pipeline_api.input_sets_v0
======================================================
Inputsets API client for Harness SDK.

Provides CRUD operations for inputset resources.

Classes
-------

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