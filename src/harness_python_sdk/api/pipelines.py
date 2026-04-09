"""
Pipelines API client for Harness SDK.

Provides CRUD operations for pipeline resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.pipelines import (
    PipelineCreateRequest,
    PipelineResponse,
    PipelineUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class PipelinesApi:
    """API client for pipeline operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize PipelinesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[PipelineResponse]:
        """List pipelines in the specified scope.

        Args:
            scope: Scope containing org and project. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm, filter_identifier).

        Yields:
            PipelineResponse: Individual pipeline items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/pipelines",
            resolved,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=PipelineResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
        )

    def get(self, pipeline_id: str, scope: Scope | None = None) -> PipelineResponse:
        """Get a single pipeline by ID.

        Args:
            pipeline_id: Pipeline identifier.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            PipelineResponse: The requested pipeline.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/pipelines/{pipeline_id}",
            resolved,
            pipeline_id=pipeline_id,
        )
        return self._client._get(
            url, params=None, response_model=PipelineResponse
        )

    def create(
        self, body: PipelineCreateRequest, scope: Scope | None = None
    ) -> PipelineResponse:
        """Create a new pipeline.

        Args:
            body: Pipeline creation request with required fields.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            PipelineResponse: The created pipeline.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/pipelines",
            resolved,
        )
        return self._client._post(
            url, params=None, body=body, response_model=PipelineResponse
        )

    def update(
        self,
        pipeline_id: str,
        body: PipelineUpdateRequest,
        scope: Scope | None = None,
    ) -> PipelineResponse:
        """Update an existing pipeline.

        Args:
            pipeline_id: Pipeline identifier.
            body: Pipeline update request with updated fields.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            PipelineResponse: The updated pipeline.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/pipelines/{pipeline_id}",
            resolved,
            pipeline_id=pipeline_id,
        )
        return self._client._put(
            url, params=None, body=body, response_model=PipelineResponse
        )

    def delete(
        self, pipeline_id: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a pipeline.

        Args:
            pipeline_id: Pipeline identifier.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/pipelines/{pipeline_id}",
            resolved,
            pipeline_id=pipeline_id,
        )
        return self._client._delete(url, params=None, response_model=None)
