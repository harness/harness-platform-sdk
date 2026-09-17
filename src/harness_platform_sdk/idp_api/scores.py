"""Scoress API client for Harness SDK.

Provides CRUD operations for scores resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.models.idp_api.scores import (
    ScoreResponse,
    ScoreSummaryResponse,
)
from harness_platform_sdk.pagination import PaginationStyle
from harness_platform_sdk.scope import Scope


class ScoreApi:
    """API client for scores operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ScoreApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        """Get the root API path for score endpoints.

        Returns:
            str: The base API path for score operations.
        """
        return "/v1/scores"

    @property
    def wrap_key(self) -> str:
        """Get the wrap key for score request bodies.

        Returns:
            str: The key used to wrap score data in API requests, or None if not used.
        """
        return None

    @property
    def unwrap_key(self) -> str:
        """Get the response unwrap key for score data.

        Returns:
            str: The key used to extract score data from API responses, or None if not needed.
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
        self.idp_scope = self._client._resolve_idp_hierarchy(self.resolved_scope)

    def _wrapped_body(self, body: ScoreCreateRequest, is_yaml: bool | None = False) -> dict:
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

    def _unwrapped_response(self, unwrapped_response: dict) -> ScoreResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        return ScoreResponse(**response_obj)

    def _unwrapped_aggregated_response(self, unwrapped_response: dict) -> ScoreResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
        # 2026-07-07
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        if "entity" in response_obj:
            response_obj["identifier"] = response_obj["entity"]["title"]
            response_obj["kind"] = response_obj["entity"]["kind"]
            response_obj["scorecard_scores"] = response_obj["entity"]["scores"]
            scores = response_obj["entity"]["scores"]
            response_obj["overall_score"] = (
                sum(s["score"] for s in scores) / len(scores) if scores else 0
            )
        del response_obj["entity"]
        return ScoreResponse(**response_obj)

    def list(
        self,
        kind: str,
        entity_type: str | None = None,
        owners: list[str] | None = None,
        tags: list[str] | None = None,
        lifecycle: list[str] | None = None,
        scope: Scope | None = None,
    ) -> ScoreResponse:
        """List scores by kind and filters.

        Args:
            kind: Entity kind.
            entity_type: Entity entity_type.
            owners: List of Entity owners.
            tags: List of Entity tags.
            lifecycle: List of Entity lifecycle.
            scope: Entity Scope . If None, uses client default scope.

        Yields:
            ScoreResponse: Individual scores items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/aggregate",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        payload = {
            "kind": kind,
            "type": entity_type,
            "owners": owners,
            "tags": tags,
            "lifecycle": lifecycle,
        }
        payload = {k: v for k, v in payload.items() if v}
        print(payload)
        print(url)
        output = self._client._paginate(
            url,
            method="post",
            body=payload,
            params=self.default_params,
            response_model=None,  # ScoreResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            # unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )

        return iter([self._unwrapped_aggregated_response(elem) for elem in output])

    def get(
        self, identifier: str, kind: str, scope: Scope | None = None, **kwargs
    ) -> Iterator[ScoreResponse]:
        """Get a single scores by Entity Identifier and Kind.

        Args:
            identifier: Entity identifier.
            kind: Entity kind.
            scope: Entity Scope . If None, uses client default scope.
            **kwargs: Additional query parameters.

        Yields:
            ScoreResponse: The requested scores.

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
        kwargs.update({"entity_identifier": "/".join([self.idp_scope, kind, identifier])})
        outputs = self._client._paginate(
            url,
            params=kwargs,
            response_model=None,  # ScoreResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self.resolved_scope,
            # unwrap_field=self.unwrap_key,  # API wraps each item in a "self.unwrap_key" field
        )

        if len(list(outputs)) <= 0:
            return []

        return_wrapper = {
            "identifier": identifier,
            "kind": kind,
        }
        return_elems = [elem | return_wrapper for elem in outputs]

        return iter([self._unwrapped_response(elem) for elem in return_elems])

    def get_summary(
        self, identifier: str, kind: str, scope: Scope | None = None
    ) -> ScoreSummaryResponse:
        """Get a summary of scores by Entity Identifier and Kind.

        Args:
            identifier: Entity identifier.
            kind: Entity kind.
            scope: Entity Scope . If None, uses client default scope.

        Returns:
            ScoreResponse: The requested scores.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/summary",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        self.default_params["entity_identifier"] = "/".join([self.idp_scope, kind, identifier])

        response = self._client._get(url, params=self.default_params, response_model=None)
        if not response:
            return {}
        if "scorecards_summary" not in response:
            return {}
        return_wrapper = {
            "identifier": identifier,
            "kind": kind,
            "account_identifier": self.resolved_scope.account_id,
            "org_identifier": self.resolved_scope.org,
            "project_identifier": self.resolved_scope.project,
        }
        return_elems = [elem | return_wrapper for elem in response["scorecards_summary"]]

        return iter([ScoreSummaryResponse(**elem) for elem in return_elems])

    def recalibrate(
        self, identifier: str, kind: str, scorecard_identifier: str, scope: Scope | None = None
    ) -> ScoreSummaryResponse:
        """API for Recalibrating the score for scorecard of entity.

        Args:
            body: Request body.
            dry_run: If True, perform a dry run without persisting changes.
            identifier: Entity identifier.
            kind: Entity kind.
            scorecard_identifier: Scorecard Identifer.
            scope: Entity Scope . If None, uses client default scope.

        Returns:
            ScoreResponse: The requested scores.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/recalibrate",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        payload = {
            "identifiers": {
                "scorecard_identifier": scorecard_identifier,
                "entity_identifier": "/".join([self.idp_scope, kind, identifier]),
            }
        }

        response = self._client._post(url, params=None, body=payload, response_model=None)
        if not response:
            return {}
        return_wrapper = {
            "identifier": identifier,
            "kind": kind,
            "account_identifier": self.resolved_scope.account_id,
            "org_identifier": self.resolved_scope.org,
            "project_identifier": self.resolved_scope.project,
        }

        unwrapped = self._client._unwrap_response(key_type="recalibrated_scores", raw_data=response)
        unwrapped = unwrapped | return_wrapper
        if "checks_statuses" in unwrapped and not unwrapped["checks_statuses"]:
            return {}
        return ScoreSummaryResponse(**unwrapped)
