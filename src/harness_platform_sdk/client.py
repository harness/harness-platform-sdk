"""Harness SDK client — main entry point for API interactions.

HarnessClient handles HTTP requests, scope resolution, URL construction,
error handling, and pagination. Supports both context manager and explicit close().
"""

import json
import time
from typing import Any, Callable, Generator, TypeVar
from urllib.parse import parse_qs

import httpx
import tenacity
import yaml
from tenacity import retry, stop_after_attempt, wait_exponential

from .base_model import HarnessModel
from .config import HarnessConfig
from .exceptions import ApiError, AuthError, ScopeNotSetError
from .pagination import PaginationStyle
from .scope import Scope

T = TypeVar("T")


class HarnessClient:
    """Main SDK client for interacting with Harness APIs.

    The client supports keyword argument construction for convenience:
        client = HarnessClient(api_key="...", account_id="...")

    Or via explicit config:
        config = HarnessConfig(api_key="...", account_id="...")
        client = HarnessClient(config=config)

    Supports both context manager and explicit close():
        with HarnessClient(...) as client:
            ...

        client = HarnessClient(...)
        try:
            ...
        finally:
            client.close()
    """

    def __init__(
        self,
        config: HarnessConfig | None = None,
        api_key: str | None = None,
        account_id: str | None = None,
        default_org: str | None = None,
        default_project: str | None = None,
        base_url: str | None = None,
    ):
        """Initialize HarnessClient.

        Can be initialized with either explicit config or with keyword arguments.
        Supports both context manager and explicit close() for resource cleanup.

        Args:
            config: Explicit HarnessConfig. If provided, other kwargs are ignored.
            api_key: API key (used if config not provided).
            account_id: Account ID (used if config not provided).
            default_org: Default organization for scope resolution.
            default_project: Default project for scope resolution.
            base_url: Base URL for Harness API (used if config not provided).

        Raises:
            ValueError: If neither config nor (api_key, account_id) provided.

        Example:
            Initialize with keyword arguments::

                client = HarnessClient(
                    api_key="your_api_key",
                    account_id="your_account_id",
                    default_org="my_organization"
                )

            Initialize with explicit config::

                from harness_platform_sdk import HarnessConfig
                config = HarnessConfig(
                    api_key="your_api_key",
                    account_id="your_account_id"
                )
                client = HarnessClient(config=config)

            Use as context manager::

                with HarnessClient(api_key="key", account_id="acct") as client:
                    orgs = client.organizations.list_organizations()
        """
        if config is None:
            if api_key is None or account_id is None:
                raise ValueError("Either config or (api_key, account_id) required")
            config_kwargs = {"api_key": api_key, "account_id": account_id}
            if base_url is not None:
                config_kwargs["base_url"] = base_url
            self._config = HarnessConfig(**config_kwargs)
        else:
            # If base_url kwarg is provided, it takes precedence over config's value
            if base_url is not None:
                self._config = config.model_copy(update={"base_url": base_url})
            else:
                self._config = config

        # Build HTTP client with retry transport
        self._http_client = self._build_http_client()

        # Set up default scope
        self._default_scope = Scope(
            account_id=self._config.account_id,
            org=default_org,
            project=default_project,
        )
        self.account_id = self._config.account_id

    def __enter__(self) -> "HarnessClient":
        """Context manager entry.

        Returns:
            Self (HarnessClient instance).
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Context manager exit.

        Closes underlying HTTP client on exit.

        Args:
            exc_type: Exception type if raised in context.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.

        Returns:
            False to propagate any exception.
        """
        self.close()
        return False

    def _build_http_client(self) -> httpx.Client:
        """Build and return a new httpx.Client with current config.

        Returns:
            A new httpx.Client configured with current settings.
        """
        transport = httpx.HTTPTransport(retries=self._config.max_retries)
        return httpx.Client(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
            transport=transport,
            headers={
                "x-api-key": self._config.api_key,
                "x-account-id": self._config.account_id,
                "Content-Type": "application/json",
            },
            verify=self._config.verify_ssl,
        )

    def close(self) -> None:
        """Close the underlying HTTP client.

        Closes the httpx.Client and releases any open connections.
        """
        if self._http_client:
            self._http_client.close()

    def __repr__(self) -> str:
        """Return representation without exposing API key."""
        return (
            f"HarnessClient(account_id={self._config.account_id!r}, "
            f"base_url={self._config.base_url!r})"
        )

    def _display_payload(self, data: Any) -> Any:
        """Debug testing method to quickly validate payload responses.

        Args:
            data: Payload data to display (any type).

        Returns:
            None (prints to stdout).
        """
        import json

        import yaml

        retries = 0
        max_tries = 3
        error = None
        print(f"{' DEBUG PAYLOAD - BEGIN ':#^40}")
        while True:
            try:
                if isinstance(data, str):
                    print(f" {data} ")
                elif isinstance(data, int):
                    print(f" {data} ")
                elif isinstance(data, list):
                    print(json.dumps(data, indent=4, sort_keys=True))
                elif isinstance(data, dict):
                    print(json.dumps(data, indent=4, sort_keys=True))
                else:
                    print(json.dumps(dict(data), indent=4, sort_keys=True))
                break
            except TypeError as err:
                try:
                    data = data.json()
                except Exception as err:
                    retries = max_tries + 1
                    raise Exception from err
            except json.JSONDecodeError as err:
                try:
                    data = yaml.safe_load(data)
                except Exception as err:
                    retries = max_tries + 1
                    raise Exception from err
            except Exception as err:
                raise Exception from err
            finally:
                retries += 1
                if retries > max_tries:
                    raise Exception("Display Failure. Unknown Handler")

        print(f"{' DEBUG PAYLOAD - END ':#^40}")

    @property
    def base_url(self) -> str:
        """Get the base URL for the Harness API.

        Returns:
            Base URL string.
        """
        return self._config.base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        """Set the base URL for the Harness API.

        Closes the existing httpx session and opens a new one with the updated URL.

        Args:
            value: New base URL for the Harness API.
        """
        self.close()
        self._config = self._config.model_copy(update={"base_url": value})
        self._http_client = self._build_http_client()

    def set_default_scope(self, org: str | None = None, project: str | None = None) -> None:
        """Update the default scope for requests.

        Args:
            org: New default organization.
            project: New default project.

        Raises:
            Exception: If project is set without org.
        """
        if project and not org:
            raise Exception(
                f"Error: Unable to create 'default_scope' for 'project' {project} as no 'org' provided."
            )
        self._default_scope = Scope(
            account_id=self._config.account_id,
            org=org,
            project=project,
        )

    def _resolve_scope(self, scope: Scope | None) -> Scope:
        """Resolve scope by merging call-time and default scopes.

        Merges the provided scope with default scope values, with call-time
        scope taking precedence over defaults.

        Args:
            scope: Call-time scope (takes precedence). If None, uses default scope.

        Returns:
            Resolved Scope with all required fields.

        Raises:
            ScopeNotSetError: If account_id is missing after resolution.
        """
        if scope is None:
            scope = self._default_scope

        # Merge with defaults if call-time scope doesn't override
        account_id = scope.account_id or self._default_scope.account_id
        org = scope.org or self._default_scope.org
        project = scope.project or self._default_scope.project
        pipeline = scope.pipeline or self._default_scope.pipeline

        if not account_id:
            raise ScopeNotSetError("account_id not set in scope or config")

        return Scope(account_id=account_id, org=org, project=project, pipeline=pipeline)

    def _resolve_hierarchy(self, scope: Scope | None) -> dict[str, str]:
        """Resolve hierarchy by current scope and return as a dict.

        Returns a dictionary with account, org, project, and pipeline identifiers
        as required by the Harness API.

        Args:
            scope: Call-time scope (takes precedence). If None, uses default.

        Returns:
            Dictionary with keys: accountIdentifier, orgIdentifier (optional),
            projectIdentifier (optional), pipelineIdentifier (optional).

        Raises:
            ScopeNotSetError: If account_id is missing.
        """
        if scope is None:
            scope = self._default_scope

        output = {
            "accountIdentifier": scope.account_id,
        }
        if scope.org:
            output["orgIdentifier"] = scope.org
        if scope.project:
            output["projectIdentifier"] = scope.project
        if scope.pipeline:
            output["pipelineIdentifier"] = scope.pipeline

        return output

    def _resolve_idp_hierarchy(self, scope: Scope | None) -> str:
        """Resolve IDP hierarchy by current scope and return as a dot-separated string.

        Builds IDP hierarchy string like "account.org.project" or "account.org".

        Args:
            scope: Call-time scope (takes precedence). If None, uses default.

        Returns:
            Dot-separated hierarchy string (e.g., "account", "account.org",
            "account.org.project").

        Raises:
            ScopeNotSetError: If account_id is missing.
        """
        if scope is None:
            scope = self._default_scope

        output = "account"
        if scope.org and scope.project:
            output = ".".join([output, scope.org, scope.project])
        elif scope.org:
            output = ".".join([output, scope.org])

        return output  # .lower()

    def _build_url(
        self, path_template: str, scope: Scope, is_params: bool | None = None, **kwargs: Any
    ) -> str | dict[str, list[str]]:
        """Build full URL from path template and scope.

        Interpolates {account_id}, {org}, {project}, {pipeline}, and custom kwargs
        into the path_template. Validates that all placeholders have values.

        Args:
            path_template: URL path with {account_id}, {org}, {project} placeholders.
            scope: Resolved scope object.
            is_params: If True, parse result as query parameters (returns dict).
            **kwargs: Additional template variables to interpolate.

        Returns:
            If is_params is True: dict of parsed query parameters.
            Otherwise: full URL path string (relative to base_url).

        Raises:
            ScopeNotSetError: If a required placeholder has no value.
        """
        # Build substitution dict
        subs = {
            "account_id": scope.account_id,
            "org": scope.org,
            "project": scope.project,
            "pipeline": scope.pipeline,
            **kwargs,
        }
        # Allow for inline overrides of scope
        if "org_id" in kwargs and kwargs["org_id"] is not None:
            subs["org"] = kwargs["org_id"]
        if "project_id" in kwargs and kwargs["project_id"] is not None:
            subs["project"] = kwargs["project_id"]
        if "pipeline_id" in kwargs and kwargs["pipeline_id"] is not None:
            subs["pipeline"] = kwargs["pipeline_id"]
        # Strip subs that are None
        subs = {k: v for k, v in subs.items() if v is not None}

        # Check for missing placeholders
        import re

        placeholders = set(re.findall(r"\{(\w+)\}", path_template))
        for placeholder in placeholders:
            if subs.get(placeholder) is None:
                raise ScopeNotSetError(f"Missing required placeholder: {placeholder}")

        if is_params:
            return parse_qs(path_template.format(**subs))
        return path_template.format(**subs)

    def _raise_for_status(self, response: httpx.Response) -> bool:
        """Check response status and raise appropriate exception.

        Validates HTTP response and raises AuthError or ApiError for failures.
        Returns False for 404 responses (treated as "not found" rather than error).

        Args:
            response: httpx.Response object.

        Returns:
            True if response is successful, False for 404, raises exception otherwise.

        Raises:
            AuthError: For 401/403 responses (authentication/authorization failures).
            ApiError: For other non-2xx responses (500, 400, etc.).
        """
        if response.is_success:
            return True

        status_code = response.status_code
        body = response.text
        headers = dict(response.headers)

        if status_code in (401, 403):
            raise AuthError(status_code, body, headers)
        elif status_code in [404]:
            if response.request.method in ["POST", "PUT", "PATCH"]:
                raise ApiError(status_code, body, headers, body)
            # Ignore 404 error as missing
            return False
        # API error: status_code=400, body_length=244, payload={'status': 'FAILURE', 'code': 'RESOURCE_NOT_FOUND_EXCEPTION', 'message': 'Connector with identifier [simple_test] not found in project [demo_project] and org [test_organization].', 'correlationId': '845f76d8-6e19-431a-be13-7222bb9bde3c', 'errors': None}
        # harness_platform_sdk.exceptions.ApiError: API error: status_code=500, body_length=180, payload={'code': 'DEFAULT_ERROR_CODE', 'level': 'ERROR', 'message': 'Entity with entityRef = resource:lab not found', 'exception': None, 'failureTypes': [], 'failureSubTypes': [], 'additionalInfo': {}}
        else:
            try:
                response_payload = response.json()
                # Some apis will return a payload status as FAILURE
                if "status" in response_payload and response_payload["status"] in ["FAILURE"]:
                    # ... If there is a code in the payload, then we will check if it matches this type
                    if "code" in response_payload and response_payload["code"] in [
                        "RESOURCE_NOT_FOUND_EXCEPTION"
                    ]:
                        # 2026-04-22
                        # NOTE: If we get this response on a POST or PUT, we need to raise an exception
                        if response.request.method in ["POST", "PUT", "PATCH"]:
                            raise ApiError(status_code, body, headers, response_payload)
                        return False
                if "level" in response_payload and response_payload["level"] in ["ERROR"]:
                    # ... If there is a code in the payload, then we will check if it matches this type
                    if "code" in response_payload and response_payload["code"] in [
                        "DEFAULT_ERROR_CODE"
                    ]:
                        # 2026-04-22
                        # NOTE: If we get this response on a POST or PUT, we need to raise an exception
                        if response.request.method in ["POST", "PUT", "PATCH"]:
                            raise ApiError(status_code, body, headers, response_payload)
                        return False
            except json.decoder.JSONDecodeError:
                response_payload = None
            # if response_payload:
            #     self._display_payload(response_payload)
            raise ApiError(status_code, body, headers, response_payload)

    def _should_retry_status_code(self, status_code: int) -> bool:
        """Check if a status code should trigger a retry.

        Args:
            status_code: HTTP status code.

        Returns:
            True if should retry, False otherwise.
        """
        return self._config.retry_enabled and status_code in self._config.retry_status_codes

    def _wait_for_retry(self, response: httpx.Response, attempt: int) -> None:
        """Wait before retrying, respecting Retry-After header if present.

        Implements exponential backoff with jitter, but respects the Retry-After
        header if present in the response.

        Args:
            response: httpx.Response object.
            attempt: Current attempt number (1-indexed).
        """
        # Check for Retry-After header
        retry_after = response.headers.get("retry-after")
        if retry_after:
            try:
                wait_seconds = int(retry_after)
                time.sleep(wait_seconds)
                return
            except ValueError:
                pass

        # Exponential backoff with jitter
        wait_time = min(2 ** (attempt - 1), 10) + (attempt * 0.1)
        time.sleep(wait_time)

    def _unwrap_response(
        self, key_type: str, raw_data: dict[str, Any], scope: Scope | None = None
    ) -> dict[str, Any]:
        """Unwrap response envelope.

        Some APIs return data in an envelope structure like:
        {"key_type": {...}, "created": ..., "updated": ..., "isFavorite": ...}

        This method extracts the key_type data and merges wrapper metadata
        (account_identifier, org_identifier, project_identifier) for model construction.

        Args:
            key_type: The key to extract from response (e.g., "organization", "project").
            raw_data: The raw response dict or "data" field from API response.
            scope: Optional scope to add scope identifiers to output.

        Returns:
            Merged dict with unwrapped fields and scope metadata.
        """
        output = raw_data
        if "data" in raw_data:
            output = raw_data.get("data", {})
        if key_type is not None:
            output = output.get(key_type, {})
        else:
            key_type = "ignored"
        if scope is not None and scope.account_id:
            output["account_identifier"] = scope.account_id
        if scope is not None and scope.org:
            output["org_identifier"] = scope.org
        if scope is not None and scope.project:
            output["project_identifier"] = scope.project
        # Merge fields with sibling metadata
        return {**output}  # , **{k: v for k, v in raw_data.items() if k != key_type}}

    def _get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        response_model: type[HarnessModel] | None = None,
    ) -> dict[str, Any] | HarnessModel:
        """Perform GET request with automatic retry on transient failures.

        Handles 404 responses by returning empty dict (treated as "not found").
        Retries on configured status codes (429, 503) with exponential backoff.
        Respects Retry-After headers when present.

        Args:
            url: Request URL path (relative to base_url).
            params: Query parameters to append to URL.
            response_model: Pydantic model class for response deserialization.
                If None, returns raw dict from JSON response.

        Returns:
            If response_model provided: Deserialized model instance.
            Otherwise: Raw dict from JSON response (or empty dict for 404).

        Raises:
            AuthError: For 401 (Unauthorized) or 403 (Forbidden) responses.
            ApiError: For other non-2xx responses (500, 400, etc.).

        Example:
            Get and deserialize to model::

                from harness_platform_sdk.models.ng_api.organizations import Organization
                org_dict = client._get(
                    "/ng/api/organizations/my-org",
                    response_model=Organization
                )
                print(org_dict.name)

            Get raw response without deserialization::

                response = client._get("/ng/api/organizations/my-org")
                print(response["name"])
        """
        max_attempts = self._config.max_retries + 1
        for attempt in range(1, max_attempts + 1):
            response = self._http_client.get(url, params=params)

            # Check if we should retry based on status code
            if self._should_retry_status_code(response.status_code):
                if attempt < max_attempts:
                    self._wait_for_retry(response, attempt)
                    continue

            # Raise for non-success responses or return empty if 404
            if not self._raise_for_status(response):
                return {}
            break

        try:
            if response_model:
                return response_model(**response.json())
            return response.json()
        except Exception as err:
            status_code = response.status_code
            body = response.text
            headers = dict(response.headers)
            if status_code in [200, 204]:
                # Sometimes, the payload returns empty on a successfull delete. So
                # we will consider a valid 204 response and return empty. This was
                # chosen as the right response instead of trapping on 'json.decoder.JSONDecodeError'
                # due to the potential condition of invalid status returning the same error.
                return {}
            # ... Else, we need to raise an error.
            raise ApiError(status_code, body, headers, {})

    def _post(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        body: HarnessModel | dict[str, Any] | None = None,
        body_is_yaml: bool = False,
        response_model: type[HarnessModel] | None = None,
    ) -> dict[str, Any] | HarnessModel:
        """Perform POST request with automatic retry on transient failures.

        Supports both JSON and YAML request bodies. Retries on 429/503 with
        exponential backoff and respects Retry-After headers.

        Args:
            url: Request URL path (relative to base_url).
            params: Query parameters to append to URL.
            body: Request body as Pydantic model or dict. If model, uses model_dump().
            body_is_yaml: If True, serialize body as YAML instead of JSON.
            response_model: Pydantic model class for response deserialization.

        Returns:
            If response_model provided: Deserialized model instance.
            Otherwise: Raw dict from JSON response.

        Raises:
            AuthError: For 401 (Unauthorized) or 403 (Forbidden) responses.
            ApiError: For other non-2xx responses (500, 400, etc.).
        """
        request_body = None
        if body is not None:
            request_body = (
                body.model_dump(by_alias=True) if isinstance(body, HarnessModel) else body
            )

        max_attempts = self._config.max_retries + 1
        for attempt in range(1, max_attempts + 1):
            if body_is_yaml:
                response = self._http_client.post(url, params=params, data=yaml.dump(request_body))
            else:
                response = self._http_client.post(url, params=params, json=request_body)

            # Check if we should retry based on status code
            if self._should_retry_status_code(response.status_code):
                if attempt < max_attempts:
                    self._wait_for_retry(response, attempt)
                    continue

            # Raise for non-success responses
            self._raise_for_status(response)
            break

        try:
            output_payload = response.json()
        except json.decoder.JSONDecodeError:
            return request_body
        if "code" in output_payload and output_payload["code"] == "ENTITY_NOT_FOUND":
            raise ApiError(400, response.text, response.headers, output_payload)

        if response_model:
            return response_model(**response.json())
        return response.json()

    def _put(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        body: HarnessModel | dict[str, Any] | None = None,
        body_is_yaml: bool = False,
        response_model: type[HarnessModel] | None = None,
    ) -> dict[str, Any] | HarnessModel:
        """Perform PUT request with automatic retry on transient failures.

        Supports both JSON and YAML request bodies. Retries on 429/503 with
        exponential backoff. Used for full resource replacement operations.

        Args:
            url: Request URL path (relative to base_url).
            params: Query parameters to append to URL.
            body: Request body as Pydantic model or dict.
            body_is_yaml: If True, serialize body as YAML instead of JSON.
            response_model: Pydantic model for response deserialization.

        Returns:
            If response_model provided: Deserialized model instance.
            Otherwise: Raw dict from JSON response.

        Raises:
            AuthError: For 401/403 responses.
            ApiError: For other non-2xx responses.
        """
        request_body = None
        if body is not None:
            request_body = (
                body.model_dump(by_alias=True) if isinstance(body, HarnessModel) else body
            )

        max_attempts = self._config.max_retries + 1
        for attempt in range(1, max_attempts + 1):
            if body_is_yaml:
                response = self._http_client.put(url, params=params, data=yaml.dump(request_body))
            else:
                response = self._http_client.put(url, params=params, json=request_body)
            # Check if we should retry based on status code
            if self._should_retry_status_code(response.status_code):
                if attempt < max_attempts:
                    self._wait_for_retry(response, attempt)
                    continue

            # Raise for non-success responses
            self._raise_for_status(response)
            break

        try:
            output_payload = response.json()
        except json.decoder.JSONDecodeError:
            return request_body

        if response_model:
            return response_model(**response.json())

        return response.json()

    def _patch(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        body: HarnessModel | dict[str, Any] | None = None,
        response_model: type[HarnessModel] | None = None,
    ) -> dict[str, Any] | HarnessModel:
        """Perform PATCH request with automatic retry on transient failures.

        Retries on 429/503 with exponential backoff. Used for partial resource
        update operations.

        Args:
            url: Request URL path (relative to base_url).
            params: Query parameters to append to URL.
            body: Request body as Pydantic model or dict. Only updated fields.
            response_model: Pydantic model for response deserialization.

        Returns:
            If response_model provided: Deserialized model instance.
            Otherwise: Raw dict from JSON response.

        Raises:
            AuthError: For 401/403 responses.
            ApiError: For other non-2xx responses.
        """
        request_body = None
        if body is not None:
            request_body = (
                body.model_dump(by_alias=True) if isinstance(body, HarnessModel) else body
            )

        max_attempts = self._config.max_retries + 1
        for attempt in range(1, max_attempts + 1):
            response = self._http_client.patch(url, params=params, json=request_body)

            # Check if we should retry based on status code
            if self._should_retry_status_code(response.status_code):
                if attempt < max_attempts:
                    self._wait_for_retry(response, attempt)
                    continue

            # Raise for non-success responses
            self._raise_for_status(response)
            break

        if response_model:
            return response_model(**response.json())
        return response.json()

    def _delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        body: HarnessModel | dict[str, Any] | None = None,
        response_model: type[HarnessModel] | None = None,
    ) -> dict[str, Any] | HarnessModel:
        """Perform DELETE request with automatic retry on transient failures.

        Handles DELETE requests with optional body (some APIs require payload).
        Treats 204 No Content as success. Retries on 429/503.

        Args:
            url: Request URL path (relative to base_url).
            params: Query parameters to append to URL.
            body: Optional request body (BaseModel or dict).
            response_model: Pydantic model for response deserialization.

        Returns:
            If response_model provided: Deserialized model instance.
            If 204 No Content: Empty dict.
            Otherwise: Raw dict from JSON response.

        Raises:
            AuthError: For 401/403 responses.
            ApiError: For other non-2xx responses.
        """
        request_body = None
        max_attempts = self._config.max_retries + 1
        for attempt in range(1, max_attempts + 1):

            if body is not None:
                request_body = (
                    body.model_dump(by_alias=True) if isinstance(body, HarnessModel) else body
                )
                response = self._http_client.request(
                    "DELETE",
                    url,
                    params=params,
                    json=request_body,
                )
            else:
                response = self._http_client.delete(url, params=params)

            # Check if we should retry based on status code
            if self._should_retry_status_code(response.status_code):
                if attempt < max_attempts:
                    self._wait_for_retry(response, attempt)
                    continue

            # Raise for non-success responses
            self._raise_for_status(response)
            break

        try:
            if response_model:
                return response_model(**response.json())
            return response.json()
        except json.decoder.JSONDecodeError:
            if request_body is None:
                return {}
            return request_body
        except Exception as err:
            status_code = response.status_code
            body = response.text
            headers = dict(response.headers)
            if status_code == 204:
                # Sometimes, the payload returns empty on a successfull delete. So
                # we will consider a valid 204 response and return empty. This was
                # chosen as the right response instead of trapping on 'json.decoder.JSONDecodeError'
                # due to the potential condition of invalid status returning the same error.
                return {}
            # ... Else, we need to raise an error.
            raise ApiError(status_code, body, headers, {})

    def _paginate(
        self,
        url: str,
        method: str = "get",
        body: HarnessModel | dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        response_model: type[HarnessModel] | None = None,
        pagination_style: PaginationStyle = PaginationStyle.OFFSET,
        scope: Scope | None = None,
        unwrap_field: str | None = None,
    ) -> Generator[Any, None, None]:
        """Paginate through paginated API results.

        Handles both offset-based (pageIndex/pageSize) and cursor-based
        (pageToken/nextPageToken) pagination. Automatically extracts items
        from various response structures.

        Args:
            url: Request URL path (relative to base_url).
            method: HTTP method ("get" or "post"). Defaults to "get".
            body: Optional request body (for POST pagination).
            params: Initial query parameters. Will be updated with pagination params.
            response_model: Pydantic model to deserialize each item.
            pagination_style: Pagination strategy (PaginationStyle.OFFSET or CURSOR).
            scope: Optional scope to add to each yielded item.
            unwrap_field: Optional field name to extract from each response item.

        Yields:
            Individual items from paginated API results. If response_model
            is provided, yields deserialized model instances.

        Raises:
            AuthError: For 401/403 responses.
            ApiError: For other non-2xx responses.
        """
        if params is None:
            params = {}

        request_body = None
        if body is not None:
            request_body = (
                body.model_dump(by_alias=True) if isinstance(body, HarnessModel) else body
            )

        # Yield each item
        # 2026-04-21
        # NOTE: Before processing the payload, we will determine the hierarchy to ensure
        # the details are available for processing
        resolved_hierarchy = self._resolve_hierarchy(scope=scope)
        if pagination_style == PaginationStyle.OFFSET:
            # Offset-based pagination (pageIndex/pageSize)
            page_index = params.get("pageIndex", 0)
            page_size = params.get("pageSize", 100)

            while True:
                params["pageIndex"] = page_index
                params["pageSize"] = page_size

                if method.lower() == "post":
                    response = self._post(url, params=params, body=request_body)
                else:
                    response = self._get(url, params=params)

                # Extract items from response - handle multiple response structures:
                # 1. Direct array (pipelines: /v1/orgs/{org}/projects/{project}/pipelines)
                # 2. Nested data.content (connectors/secrets: /ng/api/*)
                if isinstance(response, list):
                    items = response
                elif isinstance(response, dict):
                    data = response
                    if "data" in response:
                        data = response.get("data")
                    if isinstance(data, dict) and "content" in data:
                        # Nested structure: response.data.content
                        items = data.get("content", [])
                    elif isinstance(data, list):
                        # Direct data array
                        items = data
                    elif isinstance(data, dict) and data:
                        # Non-empty dict - treat as single item
                        items = [data]
                    else:
                        # Empty dict or None
                        items = []
                else:
                    items = []

                if not items:
                    break

                for item in items:
                    # Unwrap nested field if specified
                    data_to_yield = item
                    # 2026-04-21
                    # NOTE: Some paginated responses do not include the the hierarchy details
                    # in their responses. This will normalize the details and return the
                    # resolved hierarchy back into the payload for each element.
                    data_to_yield.update(dict(resolved_hierarchy))
                    if unwrap_field and isinstance(item, dict):
                        data_to_yield = item.get(unwrap_field, item)

                    if response_model and not isinstance(data_to_yield, response_model):
                        yield response_model(**data_to_yield)
                    else:
                        yield data_to_yield

                # Stop if fewer items than page size
                # Check nested pagination metadata first (more accurate)
                if isinstance(response, dict) and isinstance(response.get("data"), dict):
                    page_data = response["data"]
                    page_item_count = page_data.get("pageItemCount", len(items))
                    if page_item_count < page_size:
                        break
                elif len(items) < page_size:
                    break

                page_index += 1

        elif pagination_style == PaginationStyle.CURSOR:
            # Cursor-based pagination (nextPageToken)
            next_token = params.get("pageToken")

            while True:
                if next_token:
                    params["pageToken"] = next_token
                elif "pageToken" in params:
                    del params["pageToken"]

                if method == "post":
                    response = self._post(url, params=params, body=request_body)
                else:
                    response = self._get(url, params=params)

                # Extract items and next token - handle multiple response structures
                if isinstance(response, list):
                    items = response
                    next_token = None
                elif isinstance(response, dict):
                    data = response.get("data")
                    if isinstance(data, dict) and "content" in data:
                        # Nested structure: response.data.content
                        items = data.get("content", [])
                    elif isinstance(data, list):
                        # Direct data array
                        items = data
                    else:
                        items = []
                    # Extract cursor token from response or nested data
                    next_token = response.get("pageToken")
                    if not next_token and isinstance(data, dict):
                        next_token = data.get("pageToken")
                else:
                    items = []
                    next_token = None

                if not items:
                    break

                # Yield each item
                for item in items:
                    # Unwrap nested field if specified
                    data_to_yield = item
                    # 2026-04-21
                    # NOTE: Some paginated responses do not include the the hierarchy details
                    # in their responses. This will normalize the details and return the
                    # resolved hierarchy back into the payload for each element.
                    data_to_yield.update(dict(resolved_hierarchy))
                    if unwrap_field and isinstance(item, dict):
                        data_to_yield = item.get(unwrap_field, item)

                    if response_model and not isinstance(data_to_yield, response_model):
                        yield response_model(**data_to_yield)
                    else:
                        yield data_to_yield

                if not next_token:
                    break

    @property
    def connectors(self):
        """Lazy-loaded ConnectorsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> connectors_api = client.connectors
            >>> connectors_api is not None
            True
        """
        if not hasattr(self, "_connectors"):
            from harness_platform_sdk.ng_api.connectors import ConnectorsApi

            self._connectors = ConnectorsApi(self)
        return self._connectors

    @property
    def secrets(self):
        """Lazy-loaded SecretsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> secrets_api = client.secrets
            >>> secrets_api is not None
            True
        """
        if not hasattr(self, "_secrets"):
            from harness_platform_sdk.ng_api.secrets import SecretsApi

            self._secrets = SecretsApi(self)
        return self._secrets

    @property
    def environments_v2(self):
        """Lazy-loaded InfrastructureApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> environments_api = client.environments_v2
            >>> environments_api is not None
            True
        """
        if not hasattr(self, "_environments_v2"):
            from harness_platform_sdk.ng_api.environments_v2 import EnvironmentsV2Api

            self._environments_v2 = EnvironmentsV2Api(self)
        return self._environments_v2

    @property
    def infrastructures(self):
        """Lazy-loaded InfrastructuresApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> infrastructures_api = client.infrastructures
            >>> infrastructures_api is not None
            True
        """
        if not hasattr(self, "_infrastructures"):
            from harness_platform_sdk.ng_api.infrastructures import InfrastructuresApi

            self._infrastructures = InfrastructuresApi(self)
        return self._infrastructures

    @property
    def organizations(self):
        """Lazy-loaded OrganizationsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient, Scope
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> org_api = client.organizations
            >>> org_api is not None
            True
        """
        if not hasattr(self, "_organizations"):
            from harness_platform_sdk.ng_api.organizations import OrganizationsApi

            self._organizations = OrganizationsApi(self)
        return self._organizations

    @property
    def projects(self):
        """Lazy-loaded ProjectsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> projects_api = client.projects
            >>> projects_api is not None
            True
        """
        if not hasattr(self, "_projects"):
            from harness_platform_sdk.ng_api.projects import ProjectsApi

            self._projects = ProjectsApi(self)
        return self._projects

    @property
    def services(self):
        """Lazy-loaded ServicesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> services_api = client.services
            >>> services_api is not None
            True
        """
        if not hasattr(self, "_services"):
            from harness_platform_sdk.ng_api.services import ServicesApi

            self._services = ServicesApi(self)
        return self._services

    @property
    def roles(self):
        """Lazy-loaded RolesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> roles_api = client.roles
            >>> roles_api is not None
            True
        """
        if not hasattr(self, "_roles"):
            from harness_platform_sdk.authz.roles import RolesApi

            self._roles = RolesApi(self)
        return self._roles

    @property
    def resource_groups(self):
        """Lazy-loaded ResourceGroupsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> resource_groups_api = client.resource_groups
            >>> resource_groups_api is not None
            True
        """
        if not hasattr(self, "_resource_groups"):
            from harness_platform_sdk.authz.resource_groups import ResourceGroupsApi

            self._resource_groups = ResourceGroupsApi(self)
        return self._resource_groups

    @property
    def role_assignments(self):
        """Lazy-loaded RoleAssignmentsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> role_assignments_api = client.role_assignments
            >>> role_assignments_api is not None
            True
        """
        if not hasattr(self, "_role_assignments"):
            from harness_platform_sdk.authz.role_assignments import RoleAssignmentsApi

            self._role_assignments = RoleAssignmentsApi(self)
        return self._role_assignments

    @property
    def user_groups(self):
        """Lazy-loaded UserGroupsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> user_groups_api = client.user_groups
            >>> user_groups_api is not None
            True
        """
        if not hasattr(self, "_user_groups"):
            from harness_platform_sdk.ng_api.user_groups import UserGroupsApi

            self._user_groups = UserGroupsApi(self)
        return self._user_groups

    @property
    def pipelines_v0(self):
        """Lazy-loaded PipelinesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> pipelines_api = client.pipelines_v0
            >>> pipelines_api is not None
            True
        """
        if not hasattr(self, "_pipelines_v0"):
            from harness_platform_sdk.pipeline_api.pipelines_v0 import PipelinesV0Api

            self._pipelines_v0 = PipelinesV0Api(self)
        return self._pipelines_v0

    @property
    def input_sets_v0(self):
        """Lazy-loaded InputSetsV0Api instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> input_sets_api = client.input_sets_v0
            >>> input_sets_api is not None
            True
        """
        if not hasattr(self, "_input_sets_v0"):
            from harness_platform_sdk.pipeline_api.input_sets_v0 import InputSetsV0Api

            self._input_sets_v0 = InputSetsV0Api(self)
        return self._input_sets_v0

    @property
    def triggers_v0(self):
        """Lazy-loaded TriggersV0Api instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> triggers_api = client.triggers_v0
            >>> triggers_api is not None
            True
        """
        if not hasattr(self, "_triggers_v0"):
            from harness_platform_sdk.pipeline_api.triggers_v0 import TriggersV0Api

            self._triggers_v0 = TriggersV0Api(self)
        return self._triggers_v0

    @property
    def templates_v0(self):
        """Lazy-loaded TemplatesV0Api instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> templates_api = client.templates_v0
            >>> templates_api is not None
            True
        """
        if not hasattr(self, "_templates_v0"):
            from harness_platform_sdk.template_api.templates_v0 import TemplatesV0Api

            self._templates_v0 = TemplatesV0Api(self)
        return self._templates_v0

    @property
    def workspaces(self):
        """Lazy-loaded WorkspacesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspaces_api = client.workspaces
            >>> workspaces_api is not None
            True
        """
        if not hasattr(self, "_workspaces"):
            from harness_platform_sdk.iacm_api.workspaces import WorkspacesApi

            self._workspaces = WorkspacesApi(self)
        return self._workspaces

    @property
    def workspace_approvals(self):
        """Lazy-loaded WorkspaceApprovalsApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_approvals_api = client.workspace_approvals
            >>> workspace_approvals_api is not None
            True
        """
        if not hasattr(self, "_workspace_approvals"):
            from harness_platform_sdk.iacm_api.workspace_approvals import WorkspaceApprovalsApi

            self._workspace_approvals = WorkspaceApprovalsApi(self)
        return self._workspace_approvals

    @property
    def workspace_default_pipelines(self):
        """Lazy-loaded WorkspaceDefaultPipelinesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_default_pipelines_api = client.workspace_default_pipelines
            >>> workspace_default_pipelines_api is not None
            True
        """
        if not hasattr(self, "_workspace_default_pipelines"):
            from harness_platform_sdk.iacm_api.workspace_default_pipelines import (
                WorkspaceDefaultPipelinesApi,
            )

            self._workspace_default_pipelines = WorkspaceDefaultPipelinesApi(self)
        return self._workspace_default_pipelines

    @property
    def workspace_states(self):
        """Lazy-loaded WorkspaceStatesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_states_api = client.workspace_states
            >>> workspace_states_api is not None
            True
        """
        if not hasattr(self, "_workspace_states"):
            from harness_platform_sdk.iacm_api.workspace_states import WorkspaceStatesApi

            self._workspace_states = WorkspaceStatesApi(self)
        return self._workspace_states

    @property
    def workspace_variables(self):
        """Lazy-loaded WorkspaceVariablesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> workspace_variables_api = client.workspace_variables
            >>> workspace_variables_api is not None
            True
        """
        if not hasattr(self, "_workspace_variables"):
            from harness_platform_sdk.iacm_api.workspace_variables import WorkspaceVariablesApi

            self._workspace_variables = WorkspaceVariablesApi(self)
        return self._workspace_variables

    @property
    def entities(self):
        """Lazy-loaded EntityApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> entities_api = client.entities
            >>> entities_api is not None
            True
        """
        if not hasattr(self, "_entities"):
            from harness_platform_sdk.idp_api.entities import EntityApi

            self._entities = EntityApi(self)
        return self._entities

    @property
    def catalog_custom_properties(self):
        """Lazy-loaded CatalogCustomPropertyApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> catalog_api = client.catalog_custom_properties
            >>> catalog_api is not None
            True
        """
        if not hasattr(self, "_catalog_custom_properties"):
            from harness_platform_sdk.idp_api.catalog_custom_properties import (
                CatalogCustomPropertyApi,
            )

            self._catalog_custom_properties = CatalogCustomPropertyApi(self)
        return self._catalog_custom_properties

    @property
    def scores(self):
        """Lazy-loaded ScoreApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> scores_api = client.scores
            >>> scores_api is not None
            True
        """
        if not hasattr(self, "_scores"):
            from harness_platform_sdk.idp_api.scores import ScoreApi

            self._scores = ScoreApi(self)
        return self._scores

    @property
    def variables(self):
        """Lazy-loaded VariablesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> variables_api = client.variables
            >>> variables_api is not None
            True
        """
        if not hasattr(self, "_variables"):
            from harness_platform_sdk.ng_api.variables import VariablesApi

            self._variables = VariablesApi(self)
        return self._variables

    @property
    def service_overrides(self):
        """Lazy-loaded ServiceOverridesApi instance.

        Examples:
            >>> from harness_platform_sdk import HarnessClient
            >>> client = HarnessClient(
            ...     api_key="test_key",
            ...     account_id="test_account"
            ... )
            >>> service_overrides_api = client.service_overrides
            >>> service_overrides_api is not None
            True
        """
        if not hasattr(self, "_service_overrides"):
            from harness_platform_sdk.ng_api.service_overrides import ServiceOverridesApi

            self._service_overrides = ServiceOverridesApi(self)
        return self._service_overrides
