"""ServiceOverrides API client for Harness SDK.

Provides CRUD operations for service_overrides resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.models.ng_api.service_overrides import (
    ServiceOverrideApiCreateRequest,
    ServiceOverrideCreateRequest,
    ServiceOverrideResponse,
)
from harness_platform_sdk.pagination import PaginationStyle
from harness_platform_sdk.scope import Scope


class ServiceOverridesApi:
    """API client for service_overrides operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ServiceOverridesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client
        self._config = client._config

    @property
    def root_api_path(self) -> str:
        """Get the root API path for service overrides."""
        return "/ng/api/serviceOverrides"

    @property
    def wrap_key(self) -> str:
        """Get the wrap key (None for service overrides)."""
        return None

    @property
    def unwrap_key(self) -> str:
        """Get the unwrap key (None for service overrides)."""
        return None

    @property
    def should_wrap(self) -> bool:
        """Check if response should be wrapped (False for service overrides)."""
        return False

    @property
    def default_params(self):
        """Get the Default Request Parameters configuration."""
        return getattr(self, "_default_params", None)

    @default_params.setter
    def default_params(self, resolved: Scope) -> dict:
        """Resolve Scope Variables and Set Default Params.

        Args:
            resolved: Call-time scope (takes precedence).

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
        self, body: ServiceOverrideCreateRequest, is_yaml: bool | None = False
    ) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project

        body["spec"] = {}
        for key in [
            "application_settings",
            "environment_variables",
            "config_files",
            "connection_strings",
            "manifests",
            "variables",
        ]:
            if key in body:
                if isinstance(body[key], list):
                    body["spec"][key] = self._config.merge_duplicates(body[key])
                else:
                    body["spec"][key] = body[key]
                del body[key]

        return ServiceOverrideApiCreateRequest(**body).model_dump()

    def _unwrapped_response(self, unwrapped_response: dict) -> ServiceOverrideResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        if "data" in unwrapped_response:
            response_obj = unwrapped_response["data"]
            unwrapped_response = unwrapped_response["data"]
        if "spec" in unwrapped_response:
            del response_obj["spec"]
        if "yaml" in unwrapped_response:
            raw_response_yaml = yaml.safe_load(unwrapped_response["yaml"])
            if "overrides" in raw_response_yaml:
                response_obj["application_settings"] = raw_response_yaml["overrides"].get(
                    "application_settings", {}
                )
                response_obj["environment_variables"] = raw_response_yaml["overrides"].get(
                    "environment_variables", []
                )
                response_obj["config_files"] = raw_response_yaml["overrides"].get(
                    "config_files", []
                )
                response_obj["connection_strings"] = raw_response_yaml["overrides"].get(
                    "connection_strings", {}
                )
                response_obj["manifests"] = raw_response_yaml["overrides"].get("manifests", [])
                response_obj["variables"] = raw_response_yaml["overrides"].get("variables", [])
            del response_obj["yaml"]
        return ServiceOverrideResponse(**response_obj)

    def list(
        self, override_type: str, scope: Scope | None = None, **kwargs
    ) -> Iterator[ServiceOverrideResponse]:
        """List service overrides for an environment.

        Args:
            scope: Scope containing account/org/project. If None, uses client default scope.
            override_type: Override Type identifier (e.g. ENV_GLOBAL_OVERRIDE. Required for list).
            **kwargs: Additional query parameters.

        Yields:
            ServiceOverrideResponse: Individual service override items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        self.default_params = self.resolved_scope

        params = dict(self.default_params)
        params["type"] = override_type
        params.update(kwargs)
        url = self._client._build_url(
            "{root_api_path}/v2/list",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        outputs = self._client._paginate(
            url,
            method="post",
            params=params,
            response_model=None,  # ServiceOverrideResponse,
            pagination_style=PaginationStyle.OFFSET,
            scope=self.resolved_scope,
            unwrap_field="",
        )
        return iter([self._unwrapped_response(elem) for elem in outputs])

    def get(
        self,
        environment_identifier: str,
        service_identifier: str | None = None,
        infra_identifier: str | None = None,
        scope: Scope | None = None,
        **kwargs,
    ) -> ServiceOverrideResponse:
        """Get a single service_overrides by ID.

        Args:
            environment_identifier: Environment identifier.
            service_identifier: Service identifier (optional).
            infra_identifier: Infrastructure identifier (optional).
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters.

        Returns:
            ServiceOverrideResponse: The requested service_overrides.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        self.default_params = self.resolved_scope

        params = dict(self.default_params)
        params.update(kwargs)
        override_identifier = environment_identifier
        if service_identifier:
            override_identifier = "_".join([override_identifier, service_identifier])
        if infra_identifier:
            override_identifier = "_".join([override_identifier, infra_identifier])
        if "identifier" in kwargs:
            override_identifier = kwargs["identifier"]

        url = self._client._build_url(
            "{root_api_path}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=override_identifier,
        )
        response = self._client._get(url, params=self.default_params, response_model=None)
        if not response:
            return {}

        return self._unwrapped_response(response)

    def create(
        self, body: ServiceOverrideCreateRequest, scope: Scope | None = None
    ) -> ServiceOverrideResponse:
        """Create a new service_overrides.

        Args:
            body: ServiceOverrideCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ServiceOverrideResponse: The created service_overrides.

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
        return ServiceOverrideResponse(**unwrapped)

    def update(
        self,
        identifier: str,
        body: ServiceOverrideCreateRequest,
        scope: Scope | None = None,
    ) -> ServiceOverrideResponse:
        """Update an existing service_overrides.

        Args:
            identifier: service_overrides identifier.
            body: ServiceOverrideCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            ServiceOverrideResponse: The updated service_overrides.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        response = self._client._put(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return ServiceOverrideResponse(**unwrapped)

    def delete(self, identifier: str, scope: Scope | None = None, **kwargs) -> dict | None:
        """Delete a service override.

        Args:
            identifier: Service override identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters.

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
        params = dict(self.default_params or {})
        params.update(kwargs)
        return self._client._delete(url, params=params, response_model=None)
