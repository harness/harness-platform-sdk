"""WorkspaceVariables API client for Harness SDK.

Provides CRUD operations for workspacevariabless resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.models.iacm_api.workspace_variables import (
    WorkspaceValueType,
    WorkspaceVariableCreateRequest,
    WorkspaceVariableKind,
    WorkspaceVariableResponse,
)
from harness_platform_sdk.pagination import PaginationStyle
from harness_platform_sdk.scope import Scope


class WorkspaceVariablesApi:
    """API client for workspacevariabless operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize WorkspaceVariablesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        """Get the root API path for workspace variable endpoints.

        Returns:
            str: The base API path for workspace variable operations.
        """
        return "/iacm/api"

    @property
    def wrap_key(self) -> str:
        """Get the wrap key for workspace variable request bodies.

        Returns:
            str: The key used to wrap workspace variable data in API requests, or None if not used.
        """
        return None

    @property
    def unwrap_key(self) -> str:
        """Get the response unwrap key for workspace variable data.

        Returns:
            str: The key used to extract workspace variable data from API responses, or None if not needed.
        """
        return None

    @property
    def should_wrap(self) -> bool:
        """Check if request bodies should be wrapped.

        Returns:
            bool: True if request bodies need to be wrapped before sending to API.
        """
        return False

    @property
    def default_params(self):
        """Get the Default Request Parameters configuration."""
        return getattr(self, "_default_params", None)

    @default_params.setter
    def default_params(self, resolved: Scope) -> dict:
        """Resolve Scope Variables and Set Default Params.

        Args:
            resolved: Scope containing account/org/project context.
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
        """Get the Resolved Scope configuration."""
        return getattr(self, "_resolved_scope", None)

    @resolved_scope.setter
    def resolved_scope(self, scope: Scope) -> str:
        """Resolve Scope Variables and Set Default Params.

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
        self, body: WorkspaceVariableCreateRequest, is_yaml: bool | None = False
    ) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project
        if "key" not in body or body["key"] is None:
            body["key"] = body["identifier"]

        response = {self.wrap_key: body}

        if not self.should_wrap or self.wrap_key is None:
            return body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(self, unwrapped_response: dict) -> WorkspaceVariableResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        ignored_keys = {
            "account": "account_identifier",
            "org": "org_identifier",
            "project": "project_identifier",
        }
        for key_rm, key_rp in ignored_keys.items():
            if key_rm in response_obj:
                response_obj[key_rp] = response_obj[key_rm]
                response_obj.pop(key_rm, None)
        return WorkspaceVariableResponse(**response_obj)

    def list(
        self, workspace_identifier: str, scope: Scope | None = None, **kwargs
    ) -> Iterator[WorkspaceVariableResponse]:
        """List workspacevariablesss in the specified organization.

        Args:
            workspace_identifier: Parameter.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            WorkspaceVariableResponse: Individual workspacevariabless items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)

        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{identifier}/variables",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=workspace_identifier,
        )
        outputs = self._client._paginate(
            url,
            params=kwargs,
            response_model=None,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )
        return iter([self._unwrapped_response(elem) for elem in outputs])

    def get(
        self,
        identifier: str,
        workspace_identifier: str,
        kind: WorkspaceVariableKind,
        scope: Scope | None = None,
    ) -> WorkspaceVariableResponse:
        """Get a single workspacevariabless by ID.

        Args:
            kind: Parameter.
            workspace_identifier: Parameter.
            identifier: Workspacevariables identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            WorkspaceVariableResponse: The requested workspacevariabless.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{workspace_identifier}/variables/{kind}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            workspace_identifier=workspace_identifier,
            kind=kind.value,
        )

        response = self._client._get(url, params=self.default_params, response_model=None)
        if not response:
            return {}

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )
        return WorkspaceVariableResponse(**unwrapped)

    def create(
        self, body: WorkspaceVariableCreateRequest, scope: Scope | None = None
    ) -> WorkspaceVariableResponse:
        """Create a new workspacevariabless.

        Args:
            body: WorkspaceVariableCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            WorkspaceVariableResponse: The created workspacevariabless.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{workspace_identifier}/variables",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            workspace_identifier=body.workspace_identifier,
        )

        response = self._client._post(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        # NOTE: No information is returned so we need to construct the reponse payload
        return WorkspaceVariableResponse(**body.model_dump(exclude_none=True))

    def update(
        self,
        identifier: str,
        body: WorkspaceVariableCreateRequest,
        scope: Scope | None = None,
    ) -> WorkspaceVariableResponse:
        """Update an existing workspacevariabless.

        Args:
            identifier: workspacevariabless identifier.
            body: WorkspaceVariableCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            WorkspaceVariableResponse: The updated workspacevariabless.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{workspace_identifier}/variables/{kind}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            workspace_identifier=body.workspace_identifier,
            kind=body.kind.value,
        )

        response = self._client._put(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        # NOTE: No information is returned so we need to construct the reponse payload
        return WorkspaceVariableResponse(**body.model_dump(exclude_none=True))

    def delete(
        self,
        identifier: str,
        workspace_identifier: str,
        kind: WorkspaceVariableKind,
        scope: Scope | None = None,
    ) -> dict | None:
        """Delete a workspacevariabless.

        Args:
            kind: Parameter.
            workspace_identifier: Parameter.
            identifier: workspacevariabless identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/workspaces/{workspace_identifier}/variables/{kind}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            workspace_identifier=workspace_identifier,
            kind=kind.value,
        )
        return self._client._delete(url, params=self.default_params, response_model=None)
