"""
Triggers API client for Harness SDK.

Provides CRUD operations for trigger resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.pipeline_api.triggers_v0 import (
    TriggerV0CreateRequest,
    TriggerV0Response,
    TriggerV0ListResponse,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class TriggersV0Api:
    """API client for trigger operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize TriggersApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/pipeline/api/triggers"

    @property
    def wrap_key(self) -> str:
        return "trigger"

    @property
    def unwrap_key(self) -> str:
        return "trigger"

    @property
    def should_wrap(self) -> bool:
        return True

    @property
    def default_params(self):
        """Get the Default Request Parameters configuration"""
        return getattr(self, '_default_params', None)

    @default_params.setter
    def default_params(self, resolved: Scope) -> dict:
        """ Resolve Scope Variables and Set Default Params
        Args:
            scope: Call-time scope (takes precedence).

        Returns:
            Dictionary of Parsed Querystrings from the scope

        Raises:
            ScopeNotSetError: If required fields are missing.
        """
        self._default_params = self._client._build_url("&".join([
            "accountIdentifier={account_id}",
            "orgIdentifier={org}",
            "projectIdentifier={project}",
            "targetIdentifier={pipeline}",
        ]), resolved, is_params=True)

    @property
    def resolved_scope(self):
        """Get the Resolved Scope configuration"""
        return getattr(self, '_resolved_scope', None)

    @resolved_scope.setter
    def resolved_scope(self, scope: Scope) -> str:
        """ Resolve Scope Variables and Set Default Params
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

    def _wrapped_body(self, body: InputSetV0CreateRequest) -> dict:
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
            "description": body.get("description",""),
            "tags": body.get("tags",{}),
            "accountIdentifier": body["accountIdentifier"],
            "orgIdentifier": body["orgIdentifier"],
            "projectIdentifier": body["projectIdentifier"],
            "pipelineIdentifier": body["pipeline_identifier"],
        }
        if "source" in body:
            output_body["source"] = body["source"]
            if "type" in body["source"]:
                output_body["type"] = body["source"]["type"]
        if "inputs" in body:
            output_body["inputYaml"] = yaml.dump(body["inputs"])
        ##########

        return {self.unwrap_key: output_body}

    def _unwrapped_response(self, unwrapped_response: dict) -> TriggerV0Response:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized response. Therefore,
        # we need to construct one
        response_obj = unwrapped_response
        if "yaml" in unwrapped_response:
            raw_response_yaml = yaml.safe_load(unwrapped_response["yaml"])
            response_obj = raw_response_yaml["trigger"]
            if "source" in response_obj:
                if not response_obj["source"]:
                    response_obj["source"] = {}
                else:
                    response_obj["source"] = response_obj["source"]
            if "inputYaml" in response_obj:
                if not response_obj["inputYaml"]:
                    response_obj["inputs"] = []
                else:
                    response_obj["inputs"] = yaml.safe_load(response_obj["inputYaml"])
            del response_obj["inputYaml"]
        return TriggerV0Response(**response_obj)

    def list(self, pipeline_identifier: str, scope: Scope | None = None, **kwargs) -> Iterator[TriggerV0Response]:
        """List triggers in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            TriggerV0Response: Individual trigger items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        if scope is None:
            scope = Scope(
                account_id=self._client._default_scope.account_id, pipeline=pipeline_identifier
            )
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

    def get(self, identifier: str, pipeline_identifier: str, scope: Scope | None = None) -> TriggerV0Response:
        """Get a single trigger by ID.

        Args:
            identifier: Trigger identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            TriggerV0Response: The requested trigger.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        if scope is None:
            scope = Scope(
                account_id=self._client._default_scope.account_id, pipeline=pipeline_identifier
            )
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        response = self._client._get(
            url, params=self.default_params, response_model=None
        )

        if not response:
            return {}


        unwrapped = self._client._unwrap_response(
            key_type=None, raw_data=response, scope=self.resolved_scope
        )

        return self._unwrapped_response(unwrapped_response=unwrapped)

    def create(
        self, body: TriggerV0CreateRequest, scope: Scope | None = None
    ) -> TriggerV0Response:
        """Create a new trigger.

        Args:
            body: TriggerV0CreateRequest request with required fields.
            scope: Scope containing resource scope. If None, uses client default scope.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            TriggerV0Response: The created trigger.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        if scope is None:
            scope = Scope(
                account_id=self._client._default_scope.account_id, pipeline=body.pipeline_identifier
            )

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
            body_is_yaml=True,
            response_model=None,
        )

        return TriggerV0Response(**wrapped_body[self.wrap_key])

    def update(
        self,
        identifier: str,
        body: TriggerV0CreateRequest,
        scope: Scope | None = None,
    ) -> TriggerV0Response:
        """Update an existing trigger.

        Args:
            identifier: trigger identifier.
            body: TriggerV0CreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            TriggerV0Response: The updated trigger.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        if scope is None:
            scope = Scope(
                account_id=self._client._default_scope.account_id, pipeline=body.pipeline_identifier
            )

        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}",
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

        return TriggerV0Response(**wrapped_body[self.wrap_key])

    def delete(
        self, identifier: str, pipeline_identifier: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a trigger.

        Args:
            identifier: trigger identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        if scope is None:
            scope = Scope(
                account_id=self._client._default_scope.account_id, pipeline=pipeline_identifier
            )
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )
        return self._client._delete(url, params=self.default_params, response_model=None)
