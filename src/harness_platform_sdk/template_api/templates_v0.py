"""TemplatesV0 API client for Harness SDK.

Provides CRUD operations for templates_v0 resources.
"""

from __future__ import annotations

from collections.abc import Iterator

import yaml

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.models.template_api.templates_v0 import (
    TemplateV0CreateRequest,
    TemplateV0Response,
)
from harness_platform_sdk.pagination import PaginationStyle
from harness_platform_sdk.scope import Scope


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
        """Get the root API path for template endpoints.

        Returns:
            str: The base API path for template operations.
        """
        return "/template/api/templates"

    @property
    def wrap_key(self) -> str:
        """Get the wrap key for template request bodies.

        Returns:
            str: The key used to wrap template data in API requests.
        """
        return "template"

    @property
    def unwrap_key(self) -> str:
        """Get the response unwrap key for template data.

        Returns:
            str: The key used to extract template data from API responses.
        """
        return "templateResponseDTO"

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
        param_path = ["accountIdentifier={account_id}"]
        if resolved.org is not None:
            param_path.append("orgIdentifier={org}")
        if resolved.project is not None:
            param_path.append("projectIdentifier={project}")

        self._default_params = self._client._build_url(
            "&".join(param_path),
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

    def _wrapped_body(self, body: TemplateV0CreateRequest, is_yaml: bool | None = False) -> dict:
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
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
        """Resolve and wrap the body payload to additionally inject scope details into the payload."""
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
        if "mergedYaml" in unwrapped_response:
            print("found it line 176")
            raw_response_yaml = yaml.safe_load(unwrapped_response["mergedYaml"])
            if "template" in raw_response_yaml:
                if "spec" in raw_response_yaml["template"]:
                    response_obj["template_spec"] = raw_response_yaml["template"]["spec"]
            del response_obj["mergedYaml"]
        return TemplateV0Response(**response_obj)

    def list(
        self, template_type: str | None = "All", scope: Scope | None = None, **kwargs
    ) -> Iterator[TemplateV0ListResponse]:
        """List templates_v0s in the specified organization.

        Args:
            template_type: Parameter specification.
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
            version_label: Parameter specification.
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

    def get_entity_usage(
        self,
        identifier: str,
        scope: Scope | None = None,
        page_index: int | None = None,
        page_size: int | None = None,
        **kwargs,
    ) -> dict:
        """Get entities (pipelines, stages) that reference a template.

        Args:
            identifier: Template identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            page_index: Page index for pagination.
            page_size: Page size for pagination.
            **kwargs: Additional query parameters (e.g., searchTerm, versionLabel).

        Returns:
            dict: Paginated response with entity usage data.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/entitySetupUsage/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        params = self.default_params.copy() if self.default_params else {}
        if page_index is not None:
            params["pageIndex"] = page_index
        if page_size is not None:
            params["pageSize"] = page_size
        params.update(kwargs)

        return self._client._get(url, params=params, response_model=None)

    def get_labels(self, identifier: str, scope: Scope | None = None, **kwargs) -> dict:
        """Get custom labels for template versions.

        Args:
            identifier: Template identifier.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., versionLabel).

        Returns:
            dict: Map of version labels to custom labels.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/{identifier}/labels",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        params = self.default_params.copy() if self.default_params else {}
        params.update(kwargs)

        return self._client._get(url, params=params, response_model=None)

    def refresh_and_get(
        self, identifier: str, branch: str, scope: Scope | None = None, **kwargs
    ) -> TemplateV0Response:
        """Refresh cache and fetch a template from remote git source.

        Force-refreshes the git file cache for a remote Template and returns the
        freshly fetched entity.

        Args:
            identifier: Template identifier.
            branch: Git branch name (required).
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., versionLabel, label).

        Returns:
            TemplateV0Response: The refreshed template.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/refresh-and-get/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier,
        )

        params = self.default_params.copy() if self.default_params else {}
        params["branch"] = branch
        params.update(kwargs)

        response = self._client._get(url, params=params, response_model=None)
        if not response:
            return {}

        unwrapped = self._client._unwrap_response(
            key_type=None, raw_data=response, scope=self.resolved_scope
        )

        return self._unwrapped_response(unwrapped_response=unwrapped)

    def apply_templates(
        self,
        original_entity_yaml: str,
        scope: Scope | None = None,
        check_for_access: bool | None = None,
        get_merged_yaml_with_template_field: bool | None = None,
        get_only_file_content: bool | None = None,
        yaml_version: str | None = None,
        enforce_opa_on_execution: bool | None = None,
        **kwargs,
    ) -> dict:
        """Get complete YAML with template references resolved.

        Applies template references in the provided YAML and returns the complete
        resolved YAML with all template references substituted.

        Args:
            original_entity_yaml: The YAML content with template references.
            scope: Scope containing resource scope. If None, uses client default scope.
            check_for_access: Whether to check access for referenced templates.
            get_merged_yaml_with_template_field: Include merged YAML with template field.
            get_only_file_content: Return only file content without metadata.
            yaml_version: Harness YAML version to use.
            enforce_opa_on_execution: Enforce OPA policies on execution.
            **kwargs: Additional query parameters (e.g., branch, repoIdentifier).

        Returns:
            dict: Response containing resolved YAML and metadata.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/v2/applyTemplates",
            self.resolved_scope,
            root_api_path=self.root_api_path,
        )

        params = self.default_params.copy() if self.default_params else {}
        params.update(kwargs)

        body = {"originalEntityYaml": original_entity_yaml}
        if check_for_access is not None:
            body["checkForAccess"] = check_for_access
        if get_merged_yaml_with_template_field is not None:
            body["getMergedYamlWithTemplateField"] = get_merged_yaml_with_template_field
        if get_only_file_content is not None:
            body["getOnlyFileContent"] = get_only_file_content
        if yaml_version is not None:
            body["yamlVersion"] = yaml_version
        if enforce_opa_on_execution is not None:
            body["enforceOpaOnExecution"] = enforce_opa_on_execution

        return self._client._post(url, params=params, body=body, response_model=None)

    def resolve_template(
        self,
        identifier: str,
        version: str,
        scope: Scope | None = None,
        **kwargs,
    ) -> TemplateV0Response:
        """Get complete YAML with template references resolved.

        Applies template references in the provided YAML and returns the complete
        resolved YAML with all template references substituted.

        Args:
            identifier: TemplateV0 identifier.
            version: TemplateV0 version.
            scope: Scope containing resource scope. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., getDefaultFromOtherRepo, loadFromFallbackBranch).

        Returns:
            TemplateV0Response: The requested templates_v0 merged with references.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        self.resolved_scope = scope
        url = self._client._build_url(
            "{root_api_path}/get-resolved-template/{identifier}",
            self.resolved_scope,
            root_api_path=self.root_api_path,
            identifier=identifier.replace("account.", "").replace("org.", ""),
        )

        params = self.default_params.copy() if self.default_params else {}
        params["versionLabel"] = version
        params["getDefaultFromOtherRepo"] = "true"
        params["loadFromFallbackBranch"] = "true"
        params.update(kwargs)

        response = self._client._post(
            url,
            params=self.default_params,
            body={"templatesResolvedYaml": True},
            response_model=None,
            body_is_yaml=False,
        )

        return self._unwrapped_response(unwrapped_response=response["data"])
