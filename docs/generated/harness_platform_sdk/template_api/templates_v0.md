Module harness_platform_sdk.template_api.templates_v0
=====================================================
TemplatesV0 API client for Harness SDK.

Provides CRUD operations for templates_v0 resources.

Classes
-------

`TemplatesV0Api(client: HarnessClient)`
:   API client for templates_v0 operations.
    
    Initialize TemplatesV0Api with HarnessClient.
    
    Args:
        client: HarnessClient instance for making requests.

    ### Instance variables

    `default_params`
    :   Get the Default Request Parameters configuration.

    `resolved_scope`
    :   Get the Resolved Scope configuration.

    `root_api_path: str`
    :   Get the root API path for template endpoints.
        
        Returns:
            str: The base API path for template operations.

    `should_wrap: bool`
    :   Check if request bodies should be wrapped.
        
        Returns:
            bool: True if request bodies need to be wrapped before sending to API.

    `unwrap_key: str`
    :   Get the response unwrap key for template data.
        
        Returns:
            str: The key used to extract template data from API responses.

    `wrap_key: str`
    :   Get the wrap key for template request bodies.
        
        Returns:
            str: The key used to wrap template data in API requests.

    ### Methods

    `apply_templates(self, original_entity_yaml: str, scope: Scope | None = None, check_for_access: bool | None = None, get_merged_yaml_with_template_field: bool | None = None, get_only_file_content: bool | None = None, yaml_version: str | None = None, enforce_opa_on_execution: bool | None = None, **kwargs) ‑> dict`
    :   Get complete YAML with template references resolved.
        
        Applies template references in the provided YAML and returns the complete
        resolved YAML with all template references substituted.
        
        Args:
            original_entity_yaml: The YAML content with template references.
            scope: Scope containing resource scope. If None, uses client default scope.
            check_for_access: Whether to check access for referenced templates.
            get_merged_yaml_with_template_field: Include merged YAML with template field.
            get_only_file_content: Return only file content without metadata.
            yaml_version: Harness YAML version to use.
            enforce_opa_on_execution: Enforce OPA policies on execution.
            **kwargs: Additional query parameters (e.g., branch, repoIdentifier).
        
        Returns:
            dict: Response containing resolved YAML and metadata.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `create(self, body: TemplateV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Create a new templates_v0.
        
        Args:
            body: TemplateV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.
        
        Returns:
            TemplateV0Response: The created templates_v0.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `delete(self, identifier: str, version_label: str, scope: Scope | None = None) ‑> dict | None`
    :   Delete a templates_v0.
        
        Args:
            version_label: Parameter specification.
            identifier: templates_v0 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            dict | None: Response data (typically empty for DELETE).
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get(self, identifier: str, scope: Scope | None = None) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Get a single templates_v0 by ID.
        
        Args:
            identifier: TemplateV0 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TemplateV0Response: The requested templates_v0.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get_entity_usage(self, identifier: str, scope: Scope | None = None, page_index: int | None = None, page_size: int | None = None, **kwargs) ‑> dict`
    :   Get entities (pipelines, stages) that reference a template.
        
        Args:
            identifier: Template identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            page_index: Page index for pagination.
            page_size: Page size for pagination.
            **kwargs: Additional query parameters (e.g., searchTerm, versionLabel).
        
        Returns:
            dict: Paginated response with entity usage data.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `get_labels(self, identifier: str, scope: Scope | None = None, **kwargs) ‑> dict`
    :   Get custom labels for template versions.
        
        Args:
            identifier: Template identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., versionLabel).
        
        Returns:
            dict: Map of version labels to custom labels.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `list(self, template_type: str | None = 'All', scope: Scope | None = None, **kwargs) ‑> Iterator[TemplateV0ListResponse]`
    :   List templates_v0s in the specified organization.
        
        Args:
            template_type: Parameter specification.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).
        
        Yields:
            TemplateV0ListResponse: Individual templates_v0 items across all pages.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.

    `refresh_and_get(self, identifier: str, branch: str, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Refresh cache and fetch a template from remote git source.
        
        Force-refreshes the git file cache for a remote Template and returns the
        freshly fetched entity.
        
        Args:
            identifier: Template identifier.
            branch: Git branch name (required).
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., versionLabel, label).
        
        Returns:
            TemplateV0Response: The refreshed template.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `resolve_template(self, identifier: str, version: str, scope: Scope | None = None, **kwargs) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Get complete YAML with template references resolved.
        
        Applies template references in the provided YAML and returns the complete
        resolved YAML with all template references substituted.
        
        Args:
            identifier: TemplateV0 identifier.
            version: TemplateV0 version.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., getDefaultFromOtherRepo, loadFromFallbackBranch).
        
        Returns:
            TemplateV0Response: The requested templates_v0 merged with references.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.

    `update(self, identifier: str, body: TemplateV0CreateRequest, scope: Scope | None = None) ‑> harness_platform_sdk.models.template_api.templates_v0.TemplateV0Response`
    :   Update an existing templates_v0.
        
        Args:
            identifier: templates_v0 identifier.
            body: TemplateV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.
        
        Returns:
            TemplateV0Response: The updated templates_v0.
        
        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.