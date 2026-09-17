Module harness_platform_sdk.ng_api.infrastructures
==================================================
Infrastructures API client for Harness SDK.

Provides CRUD operations for infrastructures resources.

Classes
-------

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