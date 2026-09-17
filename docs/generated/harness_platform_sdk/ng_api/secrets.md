Module harness_platform_sdk.ng_api.secrets
==========================================
Secrets API client for Harness SDK.

Provides CRUD operations for secret resources.

Classes
-------

`SecretsApi(client: HarnessClient)`
:   API client for secret operations.
    
    Initialize SecretsApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for secret endpoints.
        
        Returns:
            str: The base API path for secret operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for secret data.
        
        Returns:
            str: The key used to extract secret data from API responses.

    ### Methods

    `create(self, body: SecretCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.secrets.SecretResponse`
    :   Create a new secret.
        
        Args:
            body: SecretCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            SecretResponse: The created secret.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a secret.
        
        Args:
            identifier: secret identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.secrets.SecretResponse`
    :   Get a single secret by ID.
        
        Args:
            identifier: Secret identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            SecretResponse: The requested secret.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.secrets.SecretResponse]`
    :   List secrets in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            SecretResponse: Individual secret items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: SecretCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.secrets.SecretResponse`
    :   Update an existing secret.
        
        Args:
            identifier: secret identifier.
            body: SecretCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            SecretResponse: The updated secret.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.