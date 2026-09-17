Module harness_platform_sdk.ng_api.user_groups
==============================================
UserGroups API client for Harness SDK.

Provides CRUD operations for user_group resources.

Classes
-------

`UserGroupsApi(client: HarnessClient)`
:   API client for user_group operations.
    
    Initialize UserGroupsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for user group endpoints.
        
        Returns:
            str: The base API path for user group operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as user group request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for user group data.
        
        Returns:
            str: The key used to extract user group data from API responses, or None if no unwrapping needed.

    ### Methods

    `create(self, body: UserGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse`
    :   Create a new user_group.
        
        Args:
            body: UserGroupCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            UserGroupResponse: The created user_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a user_group.
        
        Args:
            identifier: user_group identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse`
    :   Get a single user_group by ID.
        
        Args:
            identifier: UserGroup identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            UserGroupResponse: The requested user_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse]`
    :   List user_groups in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            UserGroupResponse: Individual user_group items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: UserGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.user_groups.UserGroupResponse`
    :   Update an existing user_group.
        
        Args:
            identifier: user_group identifier.
            body: UserGroupCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            UserGroupResponse: The updated user_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.