Module harness_platform_sdk.iacm_api
====================================
Infrastructure as Code Module (IACM) API resources.

Provides APIs for managing Terraform workspaces, states, variables, and
approvals under the /iacm/ path root.

Sub-modules
-----------
* harness_platform_sdk.iacm_api.workspace_approvals
* harness_platform_sdk.iacm_api.workspace_default_pipelines
* harness_platform_sdk.iacm_api.workspace_states
* harness_platform_sdk.iacm_api.workspace_variables
* harness_platform_sdk.iacm_api.workspaces

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

`WorkspaceDefaultPipelinesApi(client: HarnessClient)`
:   API client for workspacedefaultpipeliness operations.
    
    Initialize WorkspaceDefaultPipelineApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace default pipeline endpoints.
        
        Returns:
            str: The base API path for workspace default pipeline operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace default pipeline request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace default pipeline data.
        
        Returns:
            str: The key used to extract workspace default pipeline data from API responses, or None if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace default pipeline request bodies.
        
        Returns:
            str: The key used to wrap workspace default pipeline data in API requests, or None if not used.

    ### Methods

    `delete(self, body: WorkspaceDefaultPipelineCreateRequest, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspacedefaultpipeliness.
        
        Args:
            body: Request body.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, workspace_identifier: str | None = None, operation: WorkspaceDefaultPipelineOperation | None = None, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse`
    :   Get a single workspacedefaultpipeliness by ID.
        
        Args:
            operation: Parameter.
            workspace_identifier: Workspacedefaultpipelines workspace_identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceDefaultPipelineResponse: The requested workspacedefaultpipeliness.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse]`
    :   List workspacedefaultpipelinesss in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceDefaultPipelineResponse: Individual workspacedefaultpipeliness items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, body: WorkspaceDefaultPipelineCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_default_pipelines.WorkspaceDefaultPipelineResponse`
    :   Update an existing workspacedefaultpipeliness.
        
        Args:
            identifier: workspacedefaultpipeliness identifier.
            body: WorkspaceDefaultPipelineCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceDefaultPipelineResponse: The updated workspacedefaultpipeliness.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspaceStatesApi(client: HarnessClient)`
:   API client for workspacestates operations.
    
    Initialize WorkspacestatesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace state endpoints.
        
        Returns:
            str: The base API path for workspace state operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace state request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace state data.
        
        Returns:
            str: The key used to extract workspace state data from API responses, or None if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace state request bodies.
        
        Returns:
            str: The key used to wrap workspace state data in API requests, or None if not used.

    ### Methods

    `create(self, identifier: str, body: WorkspaceStateCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_states.WorkspaceStateResponse`
    :   Create a new workspacestates.
        
        Args:
            identifier: Workspace state identifier.
            body: WorkspaceStateCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceStateResponse: The created workspacestates.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_states.WorkspaceStateResponse`
    :   Get a single workspacestates by ID.
        
        Args:
            identifier: Workspacestate identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceStateResponse: The requested workspacestates.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspaceVariablesApi(client: HarnessClient)`
:   API client for workspacevariabless operations.
    
    Initialize WorkspaceVariablesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace variable endpoints.
        
        Returns:
            str: The base API path for workspace variable operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace variable data.
        
        Returns:
            str: The key used to extract workspace variable data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for workspace variable request bodies.
        
        Returns:
            str: The key used to wrap workspace variable data in API requests, or None if not used.

    ### Methods

    `create(self, body: WorkspaceVariableCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse`
    :   Create a new workspacevariabless.
        
        Args:
            body: WorkspaceVariableCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            WorkspaceVariableResponse: The created workspacevariabless.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, workspace_identifier: str, kind: WorkspaceVariableKind, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspacevariabless.
        
        Args:
            kind: Parameter.
            workspace_identifier: Parameter.
            identifier: workspacevariabless identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, workspace_identifier: str, kind: WorkspaceVariableKind, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse`
    :   Get a single workspacevariabless by ID.
        
        Args:
            kind: Parameter.
            workspace_identifier: Parameter.
            identifier: Workspacevariables identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceVariableResponse: The requested workspacevariabless.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, workspace_identifier: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse]`
    :   List workspacevariablesss in the specified organization.
        
        Args:
            workspace_identifier: Parameter.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceVariableResponse: Individual workspacevariabless items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: WorkspaceVariableCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspace_variables.WorkspaceVariableResponse`
    :   Update an existing workspacevariabless.
        
        Args:
            identifier: workspacevariabless identifier.
            body: WorkspaceVariableCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceVariableResponse: The updated workspacevariabless.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`WorkspacesApi(client: HarnessClient)`
:   API client for workspaces operations.
    
    Initialize WorkspacesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for workspace endpoints.
        
        Returns:
            str: The base API path for workspace operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: False, as workspace request bodies do not need wrapping.

    `unwrap_key: str`
    :   Get the response unwrap key for workspace data.
        
        Returns:
            str: The key used to extract workspace data from API responses, or "none" if not used.

    `wrap_key: str`
    :   Get the wrap key for workspace request bodies.
        
        Returns:
            str: The key used to wrap workspace data in API requests, or "none" if not used.

    ### Methods

    `create(self, body: WorkspaceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse`
    :   Create a new workspaces.
        
        Args:
            body: WorkspaceCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            WorkspaceResponse: The created workspaces.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a workspaces.
        
        Args:
            identifier: workspaces identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse`
    :   Get a single workspaces by ID.
        
        Args:
            identifier: Workspace identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceResponse: The requested workspaces.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse]`
    :   List workspacess in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            WorkspaceResponse: Individual workspaces items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: WorkspaceCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.iacm_api.workspaces.WorkspaceResponse`
    :   Update an existing workspaces.
        
        Args:
            identifier: workspaces identifier.
            body: WorkspaceCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            WorkspaceResponse: The updated workspaces.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.