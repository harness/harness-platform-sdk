Module harness_platform_sdk.idp_api.scores
==========================================
Scoress API client for Harness SDK.

Provides CRUD operations for scores resources.

Classes
-------

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