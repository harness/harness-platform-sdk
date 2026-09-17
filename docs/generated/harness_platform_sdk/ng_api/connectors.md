Module harness_platform_sdk.ng_api.connectors
=============================================
Connectors API client for Harness SDK.

Provides CRUD operations for connector resources.

Classes
-------

`ConnectorsApi(client: HarnessClient)`
:   API client for connector operations.
    
    Initialize ConnectorsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for connector endpoints.
        
        Returns:
            str: The base API path for connector operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for connector data.
        
        Returns:
            str: The key used to extract connector data from API responses.

    ### Methods

    `create(self, body: ConnectorCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.connectors.ConnectorResponse`
    :   Create a new connector.
        
        Args:
            body: ConnectorCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ConnectorResponse: The created connector.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a connector.
        
        Args:
            identifier: connector identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.connectors.ConnectorResponse`
    :   Get a single connector by ID.
        
        Args:
            identifier: Connector identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ConnectorResponse: The requested connector.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.connectors.ConnectorResponse]`
    :   List connectors in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            ConnectorResponse: Individual connector items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ConnectorCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.connectors.ConnectorResponse`
    :   Update an existing connector.
        
        Args:
            identifier: connector identifier.
            body: ConnectorCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ConnectorResponse: The updated connector.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.