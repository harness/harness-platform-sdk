"""
UserGroups API client for Harness SDK.

Provides CRUD operations for user_group resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.ng_api.user_groups import (
    UserGroupCreateRequest,
    UserGroupResponse,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class UserGroupsApi:
    """API client for user_group operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize UserGroupsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/ng/api/user-groups"

    @property
    def unwrap_key(self) -> str:
        return None  # "userGroup"

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
        path_template = ["accountIdentifier={account_id}"]
        if resolved.org is not None:
            path_template.append("orgIdentifier={org}")
        if resolved.project is not None:
            path_template.append("projectIdentifier={project}")
        self._default_params = self._client._build_url(
            "&".join(path_template),
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

    def _wrapped_body(self, body: UserGroupCreateRequest) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

        if not self.should_wrap:
            return body

        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project

        return {self.unwrap_key: body}

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[UserGroupResponse]:
        """List user_groups in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            UserGroupResponse: Individual user_group items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)

        url = self._client._build_url(
            "{root_api_path}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=UserGroupResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )

    def get(self, identifier: str, scope: Scope | None = None) -> UserGroupResponse:
        """Get a single user_group by ID.

        Args:
            identifier: UserGroup identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            UserGroupResponse: The requested user_group.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        response = self._client._get(url, params=self.default_params, response_model=None)
        if not response:
            return {}

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )
        return UserGroupResponse(**unwrapped)

    def create(self, body: UserGroupCreateRequest, scope: Scope | None = None) -> UserGroupResponse:
        """Create a new user_group.

        Args:
            body: UserGroupCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            UserGroupResponse: The created user_group.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        response = self._client._post(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return UserGroupResponse(**unwrapped)

    def update(
        self,
        identifier: str,
        body: UserGroupCreateRequest,
        scope: Scope | None = None,
    ) -> UserGroupResponse:
        """Update an existing user_group.

        Args:
            identifier: user_group identifier.
            body: UserGroupCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            UserGroupResponse: The updated user_group.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        response = self._client._put(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return UserGroupResponse(**unwrapped)

    def delete(self, identifier: str, scope: Scope | None = None) -> dict | None:
        """Delete a user_group.

        Args:
            identifier: user_group identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )
        return self._client._delete(url, params=self.default_params, response_model=None)
