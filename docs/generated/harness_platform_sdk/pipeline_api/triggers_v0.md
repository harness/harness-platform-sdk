Module harness_platform_sdk.pipeline_api.triggers_v0
====================================================
Triggers API client for Harness SDK.

Provides CRUD operations for trigger resources.

Classes
-------

`TriggersV0Api(client: HarnessClient)`
:   API client for trigger operations.
    
    Initialize TriggersApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for trigger endpoints.
        
        Returns:
            str: The base API path for trigger operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for trigger data.
        
        Returns:
            str: The key used to extract trigger data from API responses.

    `wrap_key: str`
    :   Get the wrap key for trigger request bodies.
        
        Returns:
            str: The key used to wrap trigger data in API requests.

    ### Methods

    `create(self, body: TriggerV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response`
    :   Create a new trigger.
        
        Args:
            body: TriggerV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            TriggerV0Response: The created trigger.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a trigger.
        
        Args:
            pipeline_identifier: Parameter specification.
            identifier: trigger identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response`
    :   Get a single trigger by ID.
        
        Args:
            pipeline_identifier: Parameter specification.
            identifier: Trigger identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TriggerV0Response: The requested trigger.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, pipeline_identifier: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response]`
    :   List triggers in the specified organization.
        
        Args:
            pipeline_identifier: Parameter specification.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            TriggerV0Response: Individual trigger items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, body: TriggerV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.pipeline_api.triggers_v0.TriggerV0Response`
    :   Update an existing trigger.
        
        Args:
            identifier: trigger identifier.
            body: TriggerV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TriggerV0Response: The updated trigger.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.