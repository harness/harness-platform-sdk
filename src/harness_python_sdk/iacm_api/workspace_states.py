"""
Workspacestates API client for Harness SDK.

Provides CRUD operations for workspacestates resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.iacm_api.workspace_states import (
    WorkspaceStateCreateRequest,
    WorkspaceStateResponse,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class WorkspaceStatesApi:
    """API client for workspacestates operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize WorkspacestatesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/iacm/api"

    @property
    def wrap_key(self) -> str:
        return None

    @property
    def unwrap_key(self) -> str:
        return None

    @property
    def should_wrap(self) -> bool:
        return False

    @property
    def default_params(self):
        """Get the Default Request Parameters configuration"""
        return getattr(self, "_default_params", None)

    @default_params.setter
    def default_params(self, resolved: Scope) -> dict:
        """Resolve Scope Variables and Set Default Params
        Args:
            scope: Call-time scope (takes precedence).

        Returns:
            Dictionary of Parsed Querystrings from the scope

        Raises:
            ScopeNotSetError: If required fields are missing.
        """
        self._default_params = self._client._build_url(
            "&".join(
                [
                    "accountIdentifier={account_id}",
                    "orgIdentifier={org}",
                    "projectIdentifier={project}",
                ]
            ),
            resolved,
            is_params=True,
        )

    @property
    def resolved_scope(self):
        """Get the Resolved Scope configuration"""
        return getattr(self, "_resolved_scope", None)

    @resolved_scope.setter
    def resolved_scope(self, scope: Scope) -> str:
        """Resolve Scope Variables and Set Default Params
        Args:
            scope: Call-time scope (takes precedence).

        Returns:
            Resolved Scope with all required fields.

        Raises:
            ScopeNotSetError: If required fields are missing.
        """
        self._resolved_scope = self._client._resolve_scope(scope)
        # Call out to configure the default params
        self.default_params = self._resolved_scope

    def _wrapped_body(
        self, body: WorkspaceStateCreateRequest, is_yaml: bool | None = False
    ) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

        body = body.model_dump(exclude_none=True)

        response = {self.wrap_key: body}

        if not self.should_wrap or self.wrap_key is None:
            return body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(
        self, identifier: dict, unwrapped_response: dict
    ) -> WorkspaceStateResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        return WorkspaceStateResponse(**response_obj)

    def get(self, identifier: str, scope: Scope | None = None) -> WorkspaceStateResponse:
        """Get a single workspacestates by ID.

        Args:
            identifier: Workspacestate identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            WorkspaceStateResponse: The requested workspacestates.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{identifier}/terraform-backend",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )
        response = self._client._get(url, params=self.default_params, response_model=None)

        if not response:
            return {}

        return self._unwrapped_response(identifier=identifier, unwrapped_response=response)

    def create(
        self, identifier: str, body: WorkspaceStateCreateRequest, scope: Scope | None = None
    ) -> WorkspaceStateResponse:
        """Create a new workspacestates.

        Args:
            body: WorkspaceStateCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            WorkspaceStateResponse: The created workspacestates.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{identifier}/terraform-backend",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        response = self._client._post(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return WorkspaceStateResponse(**unwrapped)
