Module harness_platform_sdk.iacm_api.workspace_approvals
========================================================
WorkspaceApprovals API client for Harness SDK.

Provides CRUD operations for workspaceapprovals resources.

Classes
-------

`WorkspaceApprovalsApi(client: HarnessClient)`
:   API client for workspaceapprovals operations.
    
    Initialize WorkspaceApprovalsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace approval endpoints.
        
        Returns:
            str: The base API path for workspace approval operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace approval request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace approval data.
        
        Returns:
            str: The key used to extract workspace approval data from API responses, or None if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace approval request bodies.
        
        Returns:
            str: The key used to wrap workspace approval data in API requests, or None if not used.

    ### Methods

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspaceapprovals.
        
        Args:
            identifier: workspaceapprovals identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalResponse`
    :   Get a single workspaceapprovals by ID.
        
        Args:
            identifier: WorkspaceApproval identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceApprovalResponse: The requested workspaceapprovals.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, workspace_identifier: str, status: WorkspaceApprovalStatus | None = None, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalListResponse]`
    :   List workspaceapprovalss in the specified organization.
        
        Args:
            status: Parameter.
            workspace_identifier: Parameter.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceApprovalResponse: Individual workspaceapprovals items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: WorkspaceApprovalCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_approvals.WorkspaceApprovalResponse`
    :   Update an existing workspaceapprovals.
        
        Args:
            identifier: workspaceapprovals identifier.
            body: WorkspaceApprovalCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceApprovalResponse: The updated workspaceapprovals.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.