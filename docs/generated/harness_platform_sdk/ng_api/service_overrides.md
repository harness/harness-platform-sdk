Module harness_platform_sdk.ng_api.service_overrides
====================================================
ServiceOverrides API client for Harness SDK.

Provides CRUD operations for service_overrides resources.

Classes
-------

`ServiceOverridesApi(client: HarnessClient)`
:   API client for service_overrides operations.
    
    Initialize ServiceOverridesApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for service overrides.

    `should_wrap: bool`
    :   Check if response should be wrapped (False for service overrides).

    `unwrap_key: str`
    :   Get the unwrap key (None for service overrides).

    `wrap_key: str`
    :   Get the wrap key (None for service overrides).

    ### Methods

    `create(self, body: ServiceOverrideCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse`
    :   Create a new service_overrides.
        
        Args:
            body: ServiceOverrideCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            ServiceOverrideResponse: The created service_overrides.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, scope: Scope | None = None, **kwargs) ‑> dict | None`
    :   Delete a service override.
        
        Args:
            identifier: Service override identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, environment_identifier: str, service_identifier: str | None = None, infra_identifier: str | None = None, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse`
    :   Get a single service_overrides by ID.
        
        Args:
            environment_identifier: Environment identifier.
            service_identifier: Service identifier (optional).
            infra_identifier: Infrastructure identifier (optional).
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters.
        
        Returns:
            ServiceOverrideResponse: The requested service_overrides.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, override_type: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse]`
    :   List service overrides for an environment.
        
        Args:
            scope: Scope containing account/org/project. If None, uses client default scope.
            override_type: Override Type identifier (e.g. ENV_GLOBAL_OVERRIDE. Required for list).
            **kwargs: Additional query parameters.
        
        Yields:
            ServiceOverrideResponse: Individual service override items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: ServiceOverrideCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.ng_api.service_overrides.ServiceOverrideResponse`
    :   Update an existing service_overrides.
        
        Args:
            identifier: service_overrides identifier.
            body: ServiceOverrideCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            ServiceOverrideResponse: The updated service_overrides.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.