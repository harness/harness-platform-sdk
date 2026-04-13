"""
Projects API client for Harness SDK.

Provides CRUD operations for project resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.projects import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class ProjectsApi:
    """API client for project operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ProjectsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def _unwrap_response(self, raw_data: dict) -> dict:
        """Unwrap project response envelope.

        API returns: {"project": {...}, "created": ..., "updated": ..., "isFavorite": ...}
        Merge wrapper metadata with project data for model construction.

        Args:
            raw_data: The "data" field from API response.

        Returns:
            Merged dict with project fields + metadata.
        """
        proj = raw_data.get("project", {})
        # Merge project fields with sibling metadata
        return {**proj, **{k: v for k, v in raw_data.items() if k != "project"}}

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[ProjectResponse]:
        """List projects in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            ProjectResponse: Individual project items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects",
            resolved,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=ProjectResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
            unwrap_field="project",
        )

    def get(self, project_id: str, scope: Scope | None = None) -> ProjectResponse:
        """Get a single project by ID.

        Args:
            project_id: Project identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ProjectResponse: The requested project.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project_id}",
            resolved,
            project_id=project_id,
        )
        response = self._client._get(url, params=None, response_model=None)
        # Unwrap envelope: response["data"] contains {"project": {...}, metadata...}
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ProjectResponse(**unwrapped)

    def create(
        self, body: ProjectCreateRequest, scope: Scope | None = None
    ) -> ProjectResponse:
        """Create a new project.

        Args:
            body: Project creation request with required fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ProjectResponse: The created project.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects",
            resolved,
        )
        # Wrap request body: {"project": {...}}
        wrapped_body = {"project": body.model_dump(exclude_none=True)}
        response = self._client._post(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ProjectResponse(**unwrapped)

    def update(
        self,
        project_id: str,
        body: ProjectUpdateRequest,
        scope: Scope | None = None,
    ) -> ProjectResponse:
        """Update an existing project.

        Args:
            project_id: Project identifier.
            body: Project update request with updated fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ProjectResponse: The updated project.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project_id}",
            resolved,
            project_id=project_id,
        )
        # Wrap request body: {"project": {...}}
        wrapped_body = {"project": body.model_dump(exclude_none=True)}
        response = self._client._put(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ProjectResponse(**unwrapped)

    def delete(
        self, project_id: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a project.

        Args:
            project_id: Project identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project_id}",
            resolved,
            project_id=project_id,
        )
        return self._client._delete(url, params=None, response_model=None)
