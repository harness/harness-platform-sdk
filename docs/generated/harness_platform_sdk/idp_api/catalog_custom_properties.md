Module harness_platform_sdk.idp_api.catalog_custom_properties
=============================================================
Catalogcustompropertiess API client for Harness SDK.

Provides CRUD operations for catalog_custom_properties resources.

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