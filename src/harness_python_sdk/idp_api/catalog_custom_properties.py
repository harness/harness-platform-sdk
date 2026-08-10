"""
Catalogcustompropertiess API client for Harness SDK.

Provides CRUD operations for catalog_custom_properties resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.idp_api.catalog_custom_properties import (
    CatalogCustomPropertyCreateRequest,
    CatalogCustomPropertyResponse,
    CatalogCustomPropertyResponseByEntity,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class CatalogCustomPropertyApi:
    """API client for catalog_custom_properties operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize CatalogCustomPropertyApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        """Get the root API path for catalog custom property endpoints.

        Returns:
            str: The base API path for catalog custom property operations.
        """
        return "/v1/catalog/custom-properties"

    @property
    def wrap_key(self) -> str:
        """Get the wrap key for catalog custom property request bodies.

        Returns:
            str: The key used to wrap catalog custom property data in API requests, or None if not used.
        """
        return None

    @property
    def unwrap_key(self) -> str:
        """Get the response unwrap key for catalog custom property data.

        Returns:
            str: The key used to extract catalog custom property data from API responses, or None if not needed.
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

    def generate_entity_ref(self, identifier: str, kind: str, **kwargs):
        """Process payload to create Entity Reference ID"""
        return "/".join([":".join([kind, self.idp_scope]), identifier])

    def _wrapped_body(
        self, body: CatalogCustomPropertyCreateRequest, is_yaml: bool | None = False
    ) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project

        response = {self.wrap_key: body}

        if not self.should_wrap or self.wrap_key is None:
            return body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(self, unwrapped_response: dict) -> CatalogCustomPropertyResponse:
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
        return CatalogCustomPropertyResponse(**response_obj)

    def _unwrapped_aggregated_response(
        self, unwrapped_response: dict
    ) -> CatalogCustomPropertyResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-07-07
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        outputs = []
        if "entity_refs" in response_obj:
            for entity_ref in response_obj["entity_refs"]:
                output_obj = response_obj.copy()
                output_obj["kind"] = entity_ref["entity_ref"].split(":")[0]
                output_obj["identifier"] = entity_ref["entity_ref"].split("/")[1]
                output_obj["value"] = entity_ref["value"]
                del output_obj["entity_refs"]
                outputs.append(CatalogCustomPropertyResponse(**output_obj))
        return outputs

    def get_by_property(
        self, catalog_property: str, scope: Scope | None = None, **kwargs
    ) -> Iterator[CatalogCustomPropertyResponse]:
        """Get entities by custom_property in the specified organization.

        Args:
            catalog_property: String representation of the property to filter entities by.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            CatalogCustomPropertyResponse: Individual catalog_custom_properties items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)
        kwargs["property"] = catalog_property

        url = self._client._build_url(
            "{root_api_path}/property",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        # return self._client._paginate(
        response = self._client._get(url, params=kwargs, response_model=None)
        return_wrapper = {
            "account_identifier": self.resolved_scope.account_id,
            "org_identifier": self.resolved_scope.org,
            "project_identifier": self.resolved_scope.project,
            "catalog_property": catalog_property,
        }
        response = response | return_wrapper

        return iter([elem for elem in self._unwrapped_aggregated_response(response)])

    def get_by_entity(
        self, identifier: str, kind: str, scope: Scope | None = None, **kwargs
    ) -> CatalogCustomPropertyResponseByEntity:
        """Get entities by custom_property in the specified organization.

        Args:
            catalog_property: String representation of the property to filter entities by.
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            CatalogCustomPropertyResponse: Individual catalog_custom_properties items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)
        kwargs.update({"entity_ref": "/".join([":".join([kind, self.idp_scope]), identifier])})

        url = self._client._build_url(
            "{root_api_path}/entity",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        # return self._client._paginate(
        response = self._client._get(url, params=kwargs, response_model=None)

        return_wrapper = {
            "account_identifier": self.resolved_scope.account_id,
            "org_identifier": self.resolved_scope.org,
            "project_identifier": self.resolved_scope.project,
            "identifier": identifier,
            "kind": kind,
        }
        response = response | return_wrapper

        return CatalogCustomPropertyResponseByEntity(**response)

    def create(
        self,
        body: CatalogCustomPropertyCreateRequest,
        dry_run: bool | None = False,
        scope: Scope | None = None,
    ) -> CatalogCustomPropertyResponse:
        """Create a new catalog_custom_properties.

        Args:
            body: CatalogCustomPropertyCreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            CatalogCustomPropertyResponse: The created catalog_custom_properties.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/entity",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        payload = {
            "property": body.catalog_property,
            "value": body.value,
            "mode": body.mode,
        }
        payload["entity_ref"] = "/".join([":".join([body.kind, self.idp_scope]), body.identifier])

        print(payload)

        response = self._client._post(
            url, params=self.default_params, body=payload, response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return body

    def update(
        self,
        body: CatalogCustomPropertyCreateRequest,
        dry_run: bool | None = False,
        scope: Scope | None = None,
    ) -> CatalogCustomPropertyResponse:
        """Update an existing catalog_custom_properties.

        Args:
            identifier: catalog_custom_properties identifier.
            body: CatalogCustomPropertyCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            CatalogCustomPropertyResponse: The updated catalog_custom_properties.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/entity",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        payload = {
            "property": body.catalog_property,
            "value": body.value,
            "mode": body.mode,
        }
        payload["entity_ref"] = "/".join([":".join([body.kind, self.idp_scope]), body.identifier])

        response = self._client._post(
            url, params=self.default_params, body=payload, response_model=None
        )

        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        return body

    def delete(
        self,
        body: CatalogCustomPropertyCreateRequest,
        dry_run: bool | None = False,
        scope: Scope | None = None,
    ) -> dict | None:
        """Delete a catalog_custom_properties.

        Args:
            identifier: catalog_custom_properties identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/entity", self.resolved_scope, root_api_path=self.root_api_path
        )
        payload = {
            "property": body.catalog_property,
        }
        payload["entity_ref"] = "/".join([":".join([body.kind, self.idp_scope]), body.identifier])
        return self._client._delete(
            url, params=self.default_params, body=payload, response_model=None
        )
