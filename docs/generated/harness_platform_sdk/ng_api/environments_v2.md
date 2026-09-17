Module harness_platform_sdk.ng_api.environments_v2
==================================================
EnvironmentsV2 API client for Harness SDK.

Provides CRUD operations for environments_v2 resources.

Classes
-------

`EnvironmentsV2Api(client: HarnessClient)`
:   API client for environments_v2 operations.
    
    Initialize EnvironmentsV2Api with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for environment endpoints.
        
        Returns:
            str: The base API path for environment operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for environment data.
        
        Returns:
            str: The key used to extract environment data from API responses.

    `wrap_key: str`
    :   Get the wrap key for environment request bodies.
        
        Returns:
            str: The key used to wrap environment data in API requests, or None if no wrapping.

    ### Methods

    `create(self, body: EnvironmentV2CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response`
    :   Create a new environments_v2.
        
        Args:
            body: EnvironmentV2CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            EnvironmentV2Response: The created environments_v2.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a environments_v2.
        
        Args:
            identifier: environments_v2 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response`
    :   Get a single environments_v2 by ID.
        
        Args:
            identifier: EnvironmentV2 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EnvironmentV2Response: The requested environments_v2.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response]`
    :   List environments_v2s in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            EnvironmentV2Response: Individual environments_v2 items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: EnvironmentV2CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.environments_v2.EnvironmentV2Response`
    :   Update an existing environments_v2.
        
        Args:
            identifier: environments_v2 identifier.
            body: EnvironmentV2CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EnvironmentV2Response: The updated environments_v2.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.