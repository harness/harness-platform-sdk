"""
Variables API client for Harness SDK.

Provides CRUD operations for variables resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.ng_api.variables import (
    VariableCreateRequest,
    VariableResponse,
    VariableSpec,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class VariablesApi:
    """API client for variables operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize VariablesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/ng/api/variables"

    @property
    def wrap_key(self) -> str:
        return "variable"

    @property
    def unwrap_key(self) -> str:
        return "variable"

    @property
    def should_wrap(self) -> bool:
        return True

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

    def _wrapped_body(self, body: VariableCreateRequest, is_yaml: bool | None = False) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project
        if "spec" in body:
            spec_data = {
                "valueType": body["spec"]["value_type"],
                "type": body["spec"]["type"],
                "fixedValue": body["spec"]["fixed_value"],
            }
            body["spec"] = spec_data

        response = {self.wrap_key: body}

        if not self.should_wrap or self.wrap_key is None:
            return body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(self, unwrapped_response: dict) -> VariableResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response

        if "accountIdentifier" not in response_obj or response_obj["accountIdentifier"] is None:
            response_obj["account_identifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in response_obj or response_obj["orgIdentifier"] is None:
            response_obj["org_identifier"] = self.resolved_scope.org
        if "projectIdentifier" not in response_obj or response_obj["projectIdentifier"] is None:
            response_obj["project_identifier"] = self.resolved_scope.project
        response_obj["spec"] = VariableSpec(**response_obj["spec"])
        return VariableResponse(**response_obj)

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[VariableResponse]:
        """List variabless in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            VariableResponse: Individual variables items across all pages.

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
        outputs = self._client._paginate(
            url,
            params=kwargs,
            response_model=None,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )
        return iter([self._unwrapped_response(elem) for elem in outputs])

    def get(self, identifier: str, scope: Scope | None = None) -> VariableResponse:
        """Get a single variables by ID.

        Args:
            identifier: Variable identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            VariableResponse: The requested variables.

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
        return VariableResponse(**unwrapped)

    def create(self, body: VariableCreateRequest, scope: Scope | None = None) -> VariableResponse:
        """Create a new variables.

        Args:
            body: VariableCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            VariableResponse: The created variables.

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
        return VariableResponse(**unwrapped)

    def update(
        self,
        identifier: str,
        body: VariableCreateRequest,
        scope: Scope | None = None,
    ) -> VariableResponse:
        """Update an existing variables.

        Args:
            identifier: variables identifier.
            body: VariableCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            VariableResponse: The updated variables.

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
        return VariableResponse(**unwrapped)

    def delete(self, identifier: str, scope: Scope | None = None) -> dict | None:
        """Delete a variables.

        Args:
            identifier: variables identifier.
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
