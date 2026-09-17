Module harness_platform_sdk.idp_api
===================================
Internal Developer Portal (IDP) API resources.

Provides APIs for managing catalog entities, scores, and custom properties
under the /idp/ path root.

Sub-modules
-----------
* harness_platform_sdk.idp_api.catalog_custom_properties
* harness_platform_sdk.idp_api.entities
* harness_platform_sdk.idp_api.scores

Classes
-------

`CatalogCustomPropertyApi(client: HarnessClient)`
:   API client for catalog_custom_properties operations.
    
    Initialize CatalogCustomPropertyApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for catalog custom property endpoints.
        
        Returns:
            str: The base API path for catalog custom property operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for catalog custom property data.
        
        Returns:
            str: The key used to extract catalog custom property data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for catalog custom property request bodies.
        
        Returns:
            str: The key used to wrap catalog custom property data in API requests, or None if not used.

    ### Methods

    `create(self, body: CatalogCustomPropertyCreateRequest, dry_run: bool | None = False, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse`
    :   Create a new catalog_custom_properties.
        
        Args:
            dry_run: Parameter.
            body: CatalogCustomPropertyCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            CatalogCustomPropertyResponse: The created catalog_custom_properties.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, body: CatalogCustomPropertyCreateRequest, dry_run: bool | None = False, scope: Scope | None = None) ‑> dict | None`
    :   Delete a catalog_custom_properties.
        
        Args:
            body: Parameter.
            dry_run: Parameter.
            identifier: catalog_custom_properties identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `generate_entity_ref(self, identifier: str, kind: str, **kwargs)`
    :   Process payload to create Entity Reference ID.

    `get_by_entity(self, identifier: str, kind: str, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponseByEntity`
    :   Get entities by custom_property in the specified organization.
        
        Args:
            identifier: Property identifier.
            kind: Entity kind.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            CatalogCustomPropertyResponse: Individual catalog_custom_properties items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `get_by_property(self, catalog_property: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse]`
    :   Get entities by custom_property in the specified organization.
        
        Args:
            catalog_property: String representation of the property to filter entities by.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            CatalogCustomPropertyResponse: Individual catalog_custom_properties items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, body: CatalogCustomPropertyCreateRequest, dry_run: bool | None = False, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.catalog_custom_properties.CatalogCustomPropertyResponse`
    :   Update an existing catalog_custom_properties.
        
        Args:
            body: CatalogCustomPropertyCreateRequest request with updated fields.
            dry_run: If True, perform a dry run without persisting changes.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            CatalogCustomPropertyResponse: The updated catalog_custom_properties.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`EntityApi(client: HarnessClient)`
:   API client for entitiess operations.
    
    Initialize EntityApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for entity endpoints.
        
        Returns:
            str: The base API path for entity operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for entity data.
        
        Returns:
            str: The key used to extract entity data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for entity request bodies.
        
        Returns:
            str: The key used to wrap entity data in API requests, or None if not used.

    ### Methods

    `create(self, body: EntityCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Create a new entitiess.
        
        Args:
            body: EntityCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            EntityResponse: The created entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, kind: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a entitiess.
        
        Args:
            kind: Parameter.
            identifier: entitiess identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, kind: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Get a single entitiess by ID.
        
        Args:
            kind: Parameter.
            identifier: Entities identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EntityResponse: The requested entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, scope: Scope | None = None, recursive=False, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.entities.EntityResponse]`
    :   List entitiesss in the specified organization.
        
        Args:
            scope: Scope containing org. If None, uses client default scope.
            recursive: If True, recursively list entities.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            EntityResponse: Individual entitiess items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `update(self, identifier: str, kind: str, body: EntityCreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.entities.EntityResponse`
    :   Update an existing entitiess.
        
        Args:
            identifier: Parameter.
            kind: Parameter.
            identifier: entitiess identifier.
            body: EntityCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            EntityResponse: The updated entitiess.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

`ScoreApi(client: HarnessClient)`
:   API client for scores operations.
    
    Initialize ScoreApi with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for score endpoints.
        
        Returns:
            str: The base API path for score operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for score data.
        
        Returns:
            str: The key used to extract score data from API responses, or None if not needed.

    `wrap_key: str`
    :   Get the wrap key for score request bodies.
        
        Returns:
            str: The key used to wrap score data in API requests, or None if not used.

    ### Methods

    `get(self, identifier: str, kind: str, scope: Scope | None = None, **kwargs) ‑> Iterator[harness_platform_sdk.models.idp_api.scores.ScoreResponse]`
    :   Get a single scores by Entity Identifier and Kind.
        
        Args:
            identifier: Entity identifier.
            kind: Entity kind.
            scope: Entity Scope . If None, uses client default scope.
            **kwargs: Additional query parameters.
        
        Yields:
            ScoreResponse: The requested scores.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `get_summary(self, identifier: str, kind: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.scores.ScoreSummaryResponse`
    :   Get a summary of scores by Entity Identifier and Kind.
        
        Args:
            identifier: Entity identifier.
            kind: Entity kind.
            scope: Entity Scope . If None, uses client default scope.
        
        Returns:
            ScoreResponse: The requested scores.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, kind: str, entity_type: str | None = None, owners: list[str] | None = None, tags: list[str] | None = None, lifecycle: list[str] | None = None, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.scores.ScoreResponse`
    :   List scores by kind and filters.
        
        Args:
            kind: Entity kind.
            entity_type: Entity entity_type.
            owners: List of Entity owners.
            tags: List of Entity tags.
            lifecycle: List of Entity lifecycle.
            scope: Entity Scope . If None, uses client default scope.
        
        Yields:
            ScoreResponse: Individual scores items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `recalibrate(self, identifier: str, kind: str, scorecard_identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.idp_api.scores.ScoreSummaryResponse`
    :   API for Recalibrating the score for scorecard of entity.
        
        Args:
            body: Request body.
            dry_run: If True, perform a dry run without persisting changes.
            identifier: Entity identifier.
            kind: Entity kind.
            scorecard_identifier: Scorecard Identifer.
            scope: Entity Scope . If None, uses client default scope.
        
        Returns:
            ScoreResponse: The requested scores.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.