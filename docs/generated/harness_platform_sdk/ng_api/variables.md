Module harness_platform_sdk.ng_api.variables
============================================
Variables API client for Harness SDK.

Provides CRUD operations for variables resources.

Classes
-------

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