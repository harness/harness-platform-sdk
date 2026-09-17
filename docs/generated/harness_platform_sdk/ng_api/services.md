Module harness_platform_sdk.ng_api.services
===========================================
Services API client for Harness SDK.

Provides CRUD operations for service resources.

Classes
-------

`ServicesApi(client: HarnessClient)`
:   API client for service operations.
    
    Initialize ServicesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for service endpoints.
        
        Returns:
            str: The base API path for service operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for service data.
        
        Returns:
            str: The key used to extract service data from API responses.

    `wrap_key: str`
    :   Get the wrap key for service request bodies.
        
        Returns:
            str: The key used to wrap service data in API requests.

    ### Methods

    `create(self, body: ServiceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.services.ServiceResponse`
    :   Create a new service.
        
        Args:
            body: ServiceCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ServiceResponse: The created service.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a service.
        
        Args:
            identifier: service identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.services.ServiceResponse`
    :   Get a single service by ID.
        
        Args:
            identifier: Service identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ServiceResponse: The requested service.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.services.ServiceResponse]`
    :   List services in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ServiceResponse: Individual service items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ServiceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.services.ServiceResponse`
    :   Update an existing service.
        
        Args:
            identifier: service identifier.
            body: ServiceCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ServiceResponse: The updated service.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.