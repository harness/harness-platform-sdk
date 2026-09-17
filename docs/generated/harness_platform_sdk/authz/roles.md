Module harness_platform_sdk.authz.roles
=======================================
Roles API client for Harness SDK.

Provides CRUD operations for role resources.

Classes
-------

`RolesApi(client: HarnessClient)`
:   API client for role operations.
    
    Initialize RolesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for role endpoints.
        
        Returns:
            str: The base API path for role operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for role data.
        
        Returns:
            str: The key used to extract role data from API responses.

    ### Methods

    `create(self, body: RoleCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.roles.RoleResponse`
    :   Create a new role.
        
        Args:
            body: RoleCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            RoleResponse: The created role.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a role.
        
        Args:
            identifier: role identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.roles.RoleResponse`
    :   Get a single role by ID.
        
        Args:
            identifier: Role identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleResponse: The requested role.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.authz.roles.RoleResponse]`
    :   List roles in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            RoleResponse: Individual role items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: RoleCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.roles.RoleResponse`
    :   Update an existing role.
        
        Args:
            identifier: role identifier.
            body: RoleCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleResponse: The updated role.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.