Module harness_platform_sdk.authz.role_assignments
==================================================
RoleAssignments API client for Harness SDK.

Provides CRUD operations for role_assignment resources.

Classes
-------

`RoleAssignmentsApi(client: HarnessClient)`
:   API client for role_assignment operations.
    
    Initialize RoleAssignmentsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for role assignment endpoints.
        
        Returns:
            str: The base API path for role assignment operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as role assignment request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for role assignment data.
        
        Returns:
            str: The key used to extract role assignment data from API responses.

    ### Methods

    `create(self, body: RoleAssignmentCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse`
    :   Create a new role_assignment.
        
        Args:
            body: RoleAssignmentCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            RoleAssignmentResponse: The created role_assignment.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a role_assignment.
        
        Args:
            identifier: role_assignment identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse`
    :   Get a single role_assignment by ID.
        
        Args:
            identifier: RoleAssignment identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleAssignmentResponse: The requested role_assignment.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse]`
    :   List role_assignments in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            RoleAssignmentResponse: Individual role_assignment items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: RoleAssignmentCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.role_assignments.RoleAssignmentResponse`
    :   Update an existing role_assignment.
        
        Args:
            identifier: role_assignment identifier.
            body: RoleAssignmentCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            RoleAssignmentResponse: The updated role_assignment.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.