"""
WorkspaceDefaultPipeline API client for Harness SDK.

Provides CRUD operations for workspacedefaultpipeliness resources.
"""

from __future__ import annotations

import yaml
import time

from collections.abc import Iterator
from itertools import chain

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.iacm_api.workspace_default_pipelines import (
    WorkspaceDefaultPipelineCreateRequest,
    WorkspaceDefaultPipelineResponse,
    WorkspaceDefaultPipelineOperation,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class WorkspaceDefaultPipelinesApi:
    """API client for workspacedefaultpipeliness operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize WorkspaceDefaultPipelineApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    @property
    def root_api_path(self) -> str:
        return "/iacm/api"

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
            "projectIdentifier={project}"
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

    def _wrapped_body(self, body: WorkspaceDefaultPipelineCreateRequest, is_yaml: bool | None = False) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""

        body = body.model_dump(exclude_none=True)

        if "accountIdentifier" not in body or body["accountIdentifier"] is None:
            body["accountIdentifier"] = self.resolved_scope.account_id
        if "orgIdentifier" not in body or body["orgIdentifier"] is None:
            body["orgIdentifier"] = self.resolved_scope.org
        if "projectIdentifier" not in body or body["projectIdentifier"] is None:
            body["projectIdentifier"] = self.resolved_scope.project
        body["pipeline"] = body["pipeline_identifier"]
        if "workspace_identifier" in body and body["workspace_identifier"] is not None:
            body["workspace"] = body["workspace_identifier"]
        body["updated"] = int(time.time())

        response = {self.wrap_key: body}

        if not self.should_wrap or self.wrap_key is None:
            return body

        if is_yaml:
            return yaml.dump(response)

        return response

    def _unwrapped_response(self, unwrapped_response: dict) -> WorkspaceDefaultPipelineResponse:
        """Resolve and wrap the body payload to additionally inject scope details into the payload"""
        # 2026-04-20
        # NOTE: This is a workaround because the payload doesn't return a completely standardized
        # response. Therefore, we need to construct one.
        response_obj = unwrapped_response
        ignored_keys = {
            "account": "account_identifier",
            "org": "org_identifier",
            "project": "project_identifier",
        }
        for key_rm, key_rp in ignored_keys.items():
            if key_rm in response_obj:
                response_obj[key_rp] = response_obj[key_rm]
                response_obj.pop(key_rm,None)
        return WorkspaceDefaultPipelineResponse(**response_obj)

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[WorkspaceDefaultPipelineResponse]:
        """List workspacedefaultpipelinesss in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            WorkspaceDefaultPipelineResponse: Individual workspacedefaultpipeliness items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        self.resolved_scope = scope
        kwargs.update(self.default_params)

        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/settings/default-pipelines",
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

    def get(self, workspace_identifier: str | None = None, operation: WorkspaceDefaultPipelineOperation | None = None, scope: Scope | None = None) -> WorkspaceDefaultPipelineResponse:
        """Get a single workspacedefaultpipeliness by ID.

        Args:
            workspace_identifier: Workspacedefaultpipelines workspace_identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            WorkspaceDefaultPipelineResponse: The requested workspacedefaultpipeliness.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        if workspace_identifier is not None:
            self.default_params["workspace"] = workspace_identifier
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/settings/default-pipelines",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        response = self._client._get(
            url, params=self.default_params, response_model=None
        )

        if not response:
            return {}

        if operation is not None:
            for elem in response:
                if "operation" in elem and elem["operation"] == operation.value:
                    return self._unwrapped_response(elem)
            return {}

        return iter([self._unwrapped_response(elem) for elem in response])

    # 2026-05-13
    # NOTE: We have disabled this endpoint due to the nature of how IACM Approvals work. At this time, the creation of an
    # approval should be by an existing Pipeline execution and therefore, only the `update` action is viable.
    ######################
    # def create(
    #     self, body: WorkspaceDefaultPipelineCreateRequest, scope: Scope | None = None
    # ) -> WorkspaceDefaultPipelineResponse:
    #     """Create a new workspacedefaultpipeliness.

    #     Args:
    #         body: WorkspaceDefaultPipelineCreateRequest request with required fields.
    #         scope: Scope containing resource scope. If None, uses client default scope.
    #         scope: Scope containing org. If None, uses client default scope.

    #     Returns:
    #         WorkspaceDefaultPipelineResponse: The created workspacedefaultpipeliness.

    #     Raises:
    #         ScopeNotSetError: If scope cannot be resolved.
    #         ApiError: For non-2xx responses.
    #     """
    #     self.resolved_scope = scope
    #     url = self._client._build_url(
    #         "{root_api_path}",
    #         self.resolved_scope,
    #         root_api_path=self.root_api_path,
    #     )

    #     response = self._client._post(
    #         url, params=self.default_params, body=self._wrapped_body(body), response_model=None
    #     )

    #     unwrapped = self._client._unwrap_response(key_type=self.unwrap_key, raw_data=response)
    #     return WorkspaceDefaultPipelineResponse(**unwrapped)

    def update(
        self,
        body: WorkspaceDefaultPipelineCreateRequest,
        scope: Scope | None = None,
    ) -> WorkspaceDefaultPipelineResponse:
        """Update an existing workspacedefaultpipeliness.

        Args:
            identifier: workspacedefaultpipeliness identifier.
            body: WorkspaceDefaultPipelineCreateRequest request with updated fields.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            WorkspaceDefaultPipelineResponse: The updated workspacedefaultpipeliness.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/settings/default-pipelines",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        response = self._client._put(
            url, params=self.default_params, body=self._wrapped_body(body), response_model=None
        )

        return self._unwrapped_response(response)

    def delete(
        self,
        body: WorkspaceDefaultPipelineCreateRequest,
        scope: Scope | None = None,
    ) -> dict | None:
        """Delete a workspacedefaultpipeliness.

        Args:
            identifier: workspacedefaultpipeliness identifier.
            scope: Scope containing resource scope. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/orgs/{org}/projects/{project}/settings/default-pipelines",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )
        return self._client._delete(
            url,
            params=self.default_params,
            body=self._wrapped_body(body),
            response_model=None
        )
