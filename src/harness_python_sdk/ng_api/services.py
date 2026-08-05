"""
Services API client for Harness SDK.

Provides CRUD operations for service resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.ng_api.services import (
    ServiceCreateRequest,
    ServiceResponse,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class ServicesApi:
    """API client for service operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ServicesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/ng/api/servicesV2"

    @property
    def wrap_key(self) -> str:
        return "service"

    @property
    def unwrap_key(self) -> str:
        return "service"

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

    def _wrapped_body(self, body: ServiceCreateRequest, is_yaml: bool | None = False) -> dict:
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

        # 2026-04-21
        # NOTE: We are going to reformat the wrapped body to align to the required payload
        # for the api.
        ##########
        output_body = {
            "identifier": body["identifier"],
            "name": body["name"],
            "description": body.get("description", ""),
            "tags": body.get("tags", {}),
            # "accountIdentifier": body["accountIdentifier"],
            "orgIdentifier": body["orgIdentifier"],
            "projectIdentifier": body["projectIdentifier"],
        }
        output_yaml_body = output_body.copy()
        output_yaml_body["serviceDefinition"] = {"spec": {}, "type": body["type"]}
        if "manifests" in body:
            output_yaml_body["serviceDefinition"]["spec"]["manifests"] = body["manifests"]
        if "artifacts" in body:
            output_yaml_body["serviceDefinition"]["spec"]["artifacts"] = body["artifacts"]
        output_body["yaml"] = yaml.dump({self.wrap_key: output_yaml_body})
        ##########

        return output_body

    def _unwrapped_response(self, unwrapped_response: dict) -> ServiceResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = dict(unwrapped_response)
        if "yaml" in unwrapped_response:
            raw_response_yaml = yaml.safe_load(unwrapped_response["yaml"])
            if "service" in raw_response_yaml:
                if "serviceDefinition" in raw_response_yaml["service"]:
                    service_definition = raw_response_yaml["service"]["serviceDefinition"]
                    response_obj["type"] = service_definition["type"]
                    if "spec" in service_definition:
                        spec_definition = service_definition["spec"]
                        if "manifests" in spec_definition:
                            if not spec_definition["manifests"]:
                                response_obj["manifests"] = []
                            else:
                                response_obj["manifests"] = spec_definition["manifests"]
                        if "artifacts" in spec_definition:
                            if not spec_definition["artifacts"]:
                                response_obj["artifacts"] = []
                            else:
                                response_obj["artifacts"] = spec_definition["artifacts"]
            del response_obj["yaml"]
        return ServiceResponse(**response_obj)

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[ServiceResponse]:
        """List services in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            ServiceResponse: Individual service items across all pages.

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

    def get(self, identifier: str, scope: Scope | None = None) -> ServiceResponse:
        """Get a single service by ID.

        Args:
            identifier: Service identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            ServiceResponse: The requested service.

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
        return self._unwrapped_response(unwrapped)

    def create(self, body: ServiceCreateRequest, scope: Scope | None = None) -> ServiceResponse:
        """Create a new service.

        Args:
            body: ServiceCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ServiceResponse: The created service.

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

        wrapped_body = self._wrapped_body(body=body)
        response = self._client._post(
            url,
            params=self.default_params,
            body=wrapped_body,
            body_is_yaml=False,
            response_model=None,
        )

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )

        return self._unwrapped_response(unwrapped_response=unwrapped)

    def update(
        self,
        identifier: str,
        body: ServiceCreateRequest,
        scope: Scope | None = None,
    ) -> ServiceResponse:
        """Update an existing service.

        Args:
            identifier: service identifier.
            body: ServiceCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            ServiceResponse: The updated service.

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

        wrapped_body = self._wrapped_body(body=body)
        response = self._client._put(
            url,
            params=self.default_params,
            body=wrapped_body,
            body_is_yaml=False,
            response_model=None,
        )

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )

        return self._unwrapped_response(unwrapped_response=unwrapped)

    def delete(self, identifier: str, scope: Scope | None = None) -> dict | None:
        """Delete a service.

        Args:
            identifier: service identifier.
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
