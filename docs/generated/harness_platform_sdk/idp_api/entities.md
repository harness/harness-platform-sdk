Module harness_platform_sdk.idp_api.entities
============================================
Entitiess API client for Harness SDK.

Provides CRUD operations for entitiess resources.

Classes
-------

`EntityApi(client: HarnessClient)`
:   API client for entitiess operations.
    
    Initialize EntityApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for entity endpoints.
        
        Returns:
            str: The base API path for entity operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for entity data.
        
        Returns:
            str: The key used to extract entity data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for entity request bodies.
        
        Returns:
            str: The key used to wrap entity data in API requests, or None if not used.

    ### Methods

    `create(self, body: EntityCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Create a new entitiess.
        
        Args:
            body: EntityCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            EntityResponse: The created entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, kind: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a entitiess.
        
        Args:
            kind: Parameter.
            identifier: entitiess identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, kind: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Get a single entitiess by ID.
        
        Args:
            kind: Parameter.
            identifier: Entities identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EntityResponse: The requested entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, recursive=False, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.entities.EntityResponse]`
    :   List entitiesss in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            recursive: If True, recursively list entities.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            EntityResponse: Individual entitiess items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, kind: str, body: EntityCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Update an existing entitiess.
        
        Args:
            identifier: Parameter.
            kind: Parameter.
            identifier: entitiess identifier.
            body: EntityCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EntityResponse: The updated entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.