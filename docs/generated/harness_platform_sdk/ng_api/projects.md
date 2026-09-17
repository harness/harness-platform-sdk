Module harness_platform_sdk.ng_api.projects
===========================================
Projects API client for Harness SDK.

Provides CRUD operations for project resources.

Classes
-------

`ProjectsApi(client: HarnessClient)`
:   API client for project operations.
    
    Initialize ProjectsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for project endpoints.
        
        Returns:
            str: The base API path for project operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for project data.
        
        Returns:
            str: The key used to extract project data from API responses.

    ### Methods

    `create(self, body: ProjectCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.projects.ProjectResponse`
    :   Create a new project.
        
        Args:
            body: ProjectCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ProjectResponse: The created project.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a project.
        
        Args:
            identifier: project identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.projects.ProjectResponse`
    :   Get a single project by ID.
        
        Args:
            identifier: Project identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ProjectResponse: The requested project.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.projects.ProjectResponse]`
    :   List projects in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ProjectResponse: Individual project items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ProjectCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.projects.ProjectResponse`
    :   Update an existing project.
        
        Args:
            identifier: project identifier.
            body: ProjectCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ProjectResponse: The updated project.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.