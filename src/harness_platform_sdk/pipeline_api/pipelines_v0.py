"""Pipelines API client for Harness SDK.

Provides CRUD operations for pipeline resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.models.pipeline_api.pipelines_v0 import (
    PipelineV0CreateRequest,
    PipelineV0ListResponse,
    PipelineV0Response,
)
from harness_platform_sdk.pagination import PaginationStyle
from harness_platform_sdk.scope import Scope


class PipelinesV0Api:
    """API client for pipeline operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize PipelinesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        """Get the root API path for pipeline endpoints.

        Returns:
            str: The base API path for pipeline operations.
        """
        return "/pipeline/api/pipelines"

    @property
    def wrap_key(self) -> str:
        """Get the wrap key for pipeline request bodies.

        Returns:
            str: The key used to wrap pipeline data in API requests.
        """
        return "pipeline"

    @property
    def unwrap_key(self) -> str:
        """Get the response unwrap key for pipeline data.

        Returns:
            str: The key used to extract pipeline data from API responses, or None if not needed.
        """
        return None

    @property
    def should_wrap(self) -> bool:
        """Check if request bodies should be wrapped.

        Returns:
            bool: True if request bodies need to be wrapped before sending to API.
        """
        return True

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

    def _wrapped_body(self, body: PipelineV0CreateRequest, is_yaml: bool | None = False) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
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

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[PipelineV0Response]:
        """List pipelines in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            PipelineV0Response: Individual pipeline items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)

        url = self._client._build_url(
            "{root_api_path}/list",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        filter_body = {"filterType": "PipelineSetup"}
        return self._client._paginate(
            url,
            params=kwargs,
            method="post",
            body=filter_body,
            response_model=PipelineV0ListResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            unwrap_field=None,
            # unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )

    def get(self, identifier: str, scope: Scope | None = None) -> PipelineV0Response:
        """Get a single pipeline by ID.

        Args:
            identifier: Pipeline identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            PipelineV0Response: The requested pipeline.

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

        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized response. Therefore,
        # we need to construct one
        pipeline_obj = unwrapped
        if "yamlPipeline" in unwrapped:
            raw_pipeline_yaml = yaml.safe_load(unwrapped["yamlPipeline"])
            pipeline_obj = raw_pipeline_yaml["pipeline"]
        return PipelineV0Response(**pipeline_obj)

    def create(
        self, body: PipelineV0CreateRequest, scope: Scope | None = None
    ) -> PipelineV0Response:
        """Create a new pipeline.

        Args:
            body: PipelineV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            PipelineV0Response: The created pipeline.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/v2",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        wrapped_body = self._wrapped_body(body=body)
        response = self._client._post(
            url,
            params=self.default_params,
            body=wrapped_body,
            body_is_yaml=True,
            response_model=None,
        )

        # 2026-04-20
        # NOTE: Because the response for an UPDATE does not return any of the details about what was updated
        # we will need to merge the request payload with any `governanceMetadata` changes.... assuming that
        # it is a success
        response_payload = dict(PipelineV0Response(**wrapped_body[self.wrap_key]))
        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        response_payload.update(dict(unwrapped))
        return PipelineV0Response(**response_payload)

    def update(
        self,
        identifier: str,
        body: PipelineV0CreateRequest,
        scope: Scope | None = None,
    ) -> PipelineV0Response:
        """Update an existing pipeline.

        Args:
            identifier: pipeline identifier.
            body: PipelineV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            PipelineV0Response: The updated pipeline.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/v2/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )
        wrapped_body = self._wrapped_body(body=body)
        response = self._client._put(
            url,
            params=self.default_params,
            body=wrapped_body,
            body_is_yaml=True,
            response_model=None,
        )

        # 2026-04-20
        # NOTE: Because the response for an UPDATE does not return any of the details about what was updated
        # we will need to merge the request payload with any `governanceMetadata` changes.... assuming that
        # it is a success
        response_payload = dict(PipelineV0Response(**wrapped_body[self.wrap_key]))
        unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
        response_payload.update(dict(unwrapped))
        return PipelineV0Response(**response_payload)

    def delete(self, identifier: str, scope: Scope | None = None) -> dict | None:
        """Delete a pipeline.

        Args:
            identifier: pipeline identifier.
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
