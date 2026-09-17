Module harness_platform_sdk.authz.resource_groups
=================================================
ResourceGroups API client for Harness SDK.

Provides CRUD operations for resource_group resources.

Classes
-------

`ResourceGroupsApi(client: HarnessClient)`
:   API client for resource_group operations.
    
    Initialize ResourceGroupsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for resource group endpoints.
        
        Returns:
            str: The base API path for resource group operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for resource group data.
        
        Returns:
            str: The key used to extract resource group data from API responses.

    ### Methods

    `create(self, body: ResourceGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse`
    :   Create a new resource_group.
        
        Args:
            body: ResourceGroupCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ResourceGroupResponse: The created resource_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a resource_group.
        
        Args:
            identifier: resource_group identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse`
    :   Get a single resource_group by ID.
        
        Args:
            identifier: ResourceGroup identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ResourceGroupResponse: The requested resource_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse]`
    :   List resource_groups in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ResourceGroupResponse: Individual resource_group items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ResourceGroupCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.authz.resource_groups.ResourceGroupResponse`
    :   Update an existing resource_group.
        
        Args:
            identifier: resource_group identifier.
            body: ResourceGroupCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ResourceGroupResponse: The updated resource_group.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.