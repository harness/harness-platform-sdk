"""
Entitiess API client for Harness SDK.

Provides CRUD operations for entitiess resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.idp_api.entities import (
    EntityComponentCreateRequest,
    EntityResourceCreateRequest,
    EntityResponse,
    EntitySystemCreateRequest,
    EntityWorkflowCreateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class EntityApi:
    """API client for entitiess operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize EntityApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/v1/entities"

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
        self.idp_scope = self._client._resolve_idp_hierarchy(self.resolved_scope)

    def _wrapped_body(self, body: EntityCreateRequest, is_yaml: bool | None = False) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

        # Get the current object Class Name to handle the YAML constructs
        current_object_class_name = body.__class__.__name__
        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project

        if "apiVersion" not in body:
            body["apiVersion"] = "harness.io/v1"

        if "metadata" not in body:
            body["metadata"] = {"description": body["description"]}

        if "spec" not in body:
            body["spec"] = {"lifecycle": body["lifecycle"]}

        del body["description"]
        response = {"yaml": yaml.dump(body)}
        return response

        response = {self.wrap_key: body}

        if not self.should_wrap or self.wrap_key is None:
            return body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(self, unwrapped_response: dict) -> EntityResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        # if "yaml" in unwrapped_response:
        #     raw_response_yaml = yaml.safe_load(unwrapped_response["yaml"])
        #     if "service" in raw_response_yaml:
        #         if "serviceDefinition" in raw_response_yaml["service"]:
        #             service_definition = raw_response_yaml["service"]["serviceDefinition"]
        #             response_obj["type"] = service_definition["type"]
        #             if "spec" in service_definition:
        #                 spec_definition = service_definition["spec"]
        #                 if "manifests" in spec_definition:
        #                     if not spec_definition["manifests"]:
        #                         response_obj["manifests"] = []
        #                     else:
        #                         response_obj["manifests"] = spec_definition["manifests"]
        #                 if "artifacts" in spec_definition:
        #                     if not spec_definition["artifacts"]:
        #                         response_obj["artifacts"] = []
        #                     else:
        #                         response_obj["artifacts"] = spec_definition["artifacts"]
        #     del response_obj["yaml"]
        return EntityResponse(**response_obj)

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[EntityResponse]:
        """List entitiesss in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            EntityResponse: Individual entitiess items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)
        kwargs["scopes"] = self.idp_scope

        url = self._client._build_url(
            "{root_api_path}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=EntityResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )

    def get(self, identifier: str, kind: str, scope: Scope | None = None) -> EntityResponse:
        """Get a single entitiess by ID.

        Args:
            identifier: Entities identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            EntityResponse: The requested entitiess.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{idp_scope}/{kind}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            kind=kind,
            idp_scope=self.idp_scope,
        )

        response = self._client._get(url, params=self.default_params, response_model=None)
        if not response:
            return {}

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )
        return EntityResponse(**unwrapped)

    def create(self, body: EntityCreateRequest, scope: Scope | None = None) -> EntityResponse:
        """Create a new entitiess.

        Args:
            body: EntityCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            EntityResponse: The created entitiess.

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
        return EntityResponse(**unwrapped)

    def update(
        self,
        identifier: str,
        kind: str,
        body: EntityCreateRequest,
        scope: Scope | None = None,
    ) -> EntityResponse:
        """Update an existing entitiess.

        Args:
            identifier: entitiess identifier.
            body: EntityCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            EntityResponse: The updated entitiess.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{idp_scope}/{kind}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            kind=kind,
            idp_scope=self.idp_scope,
        )

        response = self._client._put(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return EntityResponse(**unwrapped)

    def delete(self, identifier: str, kind: str, scope: Scope | None = None) -> dict | None:
        """Delete a entitiess.

        Args:
            identifier: entitiess identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{idp_scope}/{kind}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            kind=kind,
            idp_scope=self.idp_scope,
        )
        return self._client._delete(url, params=self.default_params, response_model=None)
