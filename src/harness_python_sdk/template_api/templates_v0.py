"""
TemplatesV0 API client for Harness SDK.

Provides CRUD operations for templates_v0 resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.template_api.templates_v0 import (
    TemplateV0CreateRequest,
    TemplateV0Response,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class TemplatesV0Api:
    """API client for templates_v0 operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize TemplatesV0Api with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/template/api/templates"

    @property
    def wrap_key(self) -> str:
        return "template"

    @property
    def unwrap_key(self) -> str:
        return "templateResponseDTO"

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

    def _wrapped_body(self, body: TemplateV0CreateRequest, is_yaml: bool | None = False) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

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
            "accountIdentifier": body["accountIdentifier"],
            "orgIdentifier": body["orgIdentifier"],
            "projectIdentifier": body["projectIdentifier"],
            "type": body["template_entity_type"],
            "spec": body["template_spec"],
            "versionLabel": body["version_label"],
        }
        ##########

        response = {self.wrap_key: output_body}

        if not self.should_wrap or self.wrap_key is None:
            return output_body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(self, unwrapped_response: dict) -> TemplateV0Response:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        if "accountId" in response_obj:
            del response_obj["accountId"]
        if "yaml" in unwrapped_response:
            raw_response_yaml = yaml.safe_load(unwrapped_response["yaml"])
            if "template" in raw_response_yaml:
                if "spec" in raw_response_yaml["template"]:
                    response_obj["template_spec"] = raw_response_yaml["template"]["spec"]
            del response_obj["yaml"]
        return TemplateV0Response(**response_obj)

    def list(
        self, template_type: str | None = "All", scope: Scope | None = None, **kwargs
    ) -> Iterator[TemplateV0ListResponse]:
        """List templates_v0s in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            TemplateV0ListResponse: Individual templates_v0 items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)
        kwargs["templateListType"] = template_type

        url = self._client._build_url(
            "{root_api_path}/list-metadata",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        filter_body = {"filterType": "Template"}
        outputs = self._client._paginate(
            url,
            params=kwargs,
            method="post",
            body=filter_body,
            response_model=None,  # TemplateV0ListResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            # unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )

        return iter([self._unwrapped_response(elem) for elem in outputs])

    def get(self, identifier: str, scope: Scope | None = None) -> TemplateV0Response:
        """Get a single templates_v0 by ID.

        Args:
            identifier: TemplateV0 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            TemplateV0Response: The requested templates_v0.

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
            key_type=None, raw_data=response, scope=self.resolved_scope
        )

        return self._unwrapped_response(unwrapped_response=unwrapped)

    def create(
        self, body: TemplateV0CreateRequest, scope: Scope | None = None
    ) -> TemplateV0Response:
        """Create a new templates_v0.

        Args:
            body: TemplateV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            TemplateV0Response: The created templates_v0.

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
            url,
            params=self.default_params,
            body=self._wrapped_body(body),
            response_model=None,
            body_is_yaml=True,
        )

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )
        return self._unwrapped_response(unwrapped_response=unwrapped)

    def update(
        self,
        identifier: str,
        body: TemplateV0CreateRequest,
        scope: Scope | None = None,
    ) -> TemplateV0Response:
        """Update an existing templates_v0.

        Args:
            identifier: templates_v0 identifier.
            body: TemplateV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            TemplateV0Response: The updated templates_v0.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/update/{identifier}/{version_label}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            version_label=body.version_label,
        )

        response = self._client._put(
            url,
            params=self.default_params,
            body=self._wrapped_body(body),
            response_model=None,
            body_is_yaml=True,
        )

        unwrapped = self._client._unwrap_response(
            key_type=self.unwrap_key, raw_data=response, scope=self.resolved_scope
        )
        return self._unwrapped_response(unwrapped_response=unwrapped)

    def delete(
        self, identifier: str, version_label: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a templates_v0.

        Args:
            identifier: templates_v0 identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}/{version_label}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
            version_label=version_label,
        )
        return self._client._delete(url, params=self.default_params, response_model=None)
