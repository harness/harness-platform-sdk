"""
Harness SDK client — main entry point for API interactions.

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

        Args:
            config: Explicit HarnessConfig. If provided, other kwargs are ignored.
            api_key: API key (used if config not provided).
            account_id: Account ID (used if config not provided).
            default_org: Default organization for scope resolution.
            default_project: Default project for scope resolution.
            base_url: Base URL for Harness API (used if config not provided).
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

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
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

    def close(self):
        """Close the underlying HTTP client."""
        if self._http_client:
            self._http_client.close()

    def __repr__(self) -> str:
        """Return representation without exposing API key."""
        return (
            f"HarnessClient(account_id={self._config.account_id!r}, "
            f"base_url={self._config.base_url!r})"
        )

    def _display_payload(self, data) -> any:
        """Debug Testing Method to quickly validate payload responses"""
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
        """Get the base URL for the Harness API."""
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

    def set_default_scope(self, org: str | None = None, project: str | None = None):
        """Update the default scope for requests.

        Args:
            org: New default organization.
            project: New default project.
        """
        self._default_scope = Scope(
            account_id=self._config.account_id,
            org=org,
            project=project,
        )

    def _resolve_scope(self, scope: Scope | None) -> Scope:
        """Resolve scope by merging call-time and default scopes.

        Args:
            scope: Call-time scope (takes precedence).

        Returns:
            Resolved Scope with all required fields.

        Raises:
            ScopeNotSetError: If required fields are missing.
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

    def _resolve_hierarchy(self, scope: Scope | None) -> dict:
        """Resolve hierarchy by current scope and return as a dict.

        Args:
            scope: Call-time scope (takes precedence).

        Returns:
            Resolved Scope returned as Dictionary.

        Raises:
            ScopeNotSetError: If required fields are missing.
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

    def _build_url(
        self, path_template: str, scope: Scope, is_params: bool | None = None, **kwargs
    ) -> str:
        """Build full URL from path template and scope.

        Args:
            path_template: URL path with {account_id}, {org}, {project} placeholders.
            scope: Resolved scope.
            **kwargs: Additional template variables.

        Returns:
            Full URL path (relative to base_url).

        Raises:
            ScopeNotSetError: If a required placeholder is missing.
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
            subs["project"] = kwargs["pipeline_id"]
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

    def _raise_for_status(self, response: httpx.Response):
        """Check response status and raise appropriate exception.

        Args:
            response: httpx.Response object.

        Raises:
            AuthError: For 401/403 responses.
            ApiError: For other non-2xx responses.
        """
        if response.is_success:
            return True

        status_code = response.status_code
        body = response.text
        headers = dict(response.headers)

        if status_code in (401, 403):
            raise AuthError(status_code, body, headers)
        elif status_code in [404]:
            # Ignore 404 error as missing
            return False
        # API error: status_code=400, body_length=244, payload={'status': 'FAILURE', 'code': 'RESOURCE_NOT_FOUND_EXCEPTION', 'message': 'Connector with identifier [simple_test] not found in project [demo_project] and org [test_organization].', 'correlationId': '845f76d8-6e19-431a-be13-7222bb9bde3c', 'errors': None}
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
                        if response.request.method in ["POST","PUT","PATCH"]:
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

    def _wait_for_retry(self, response: httpx.Response, attempt: int):
        """Wait before retrying, respecting Retry-After header if present.

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

    def _unwrap_response(self, key_type: str, raw_data: dict, scope: Scope | None = None) -> dict:
        """Unwrap response envelope.

        API returns: {"key_type": {...}, "created": ..., "updated": ..., "isFavorite": ...}
        Merge wrapper metadata with key_type data for model construction.

        Args:
            raw_data: The "data" field from API response.

        Returns:
            Merged dict with fields + metadata.
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
        params: dict | None = None,
        response_model: type[HarnessModel] | None = None,
    ) -> dict | HarnessModel:
        """Perform GET request with retry.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            response_model: Pydantic model for response deserialization.

        Returns:
            Deserialized response or dict if no model provided.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
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
        params: dict | None = None,
        body: HarnessModel | dict | None = None,
        body_is_yaml: bool | None = False,
        response_model: type[HarnessModel] | None = None,
    ) -> dict | HarnessModel:
        """Perform POST request with retry.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            body: Request body (BaseModel or dict).
            response_model: Pydantic model for response deserialization.

        Returns:
            Deserialized response or dict if no model provided.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
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
            # print(f"\t RESPONSE URL: {response.url}")

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
        params: dict | None = None,
        body: HarnessModel | dict | None = None,
        body_is_yaml: bool | None = False,
        response_model: type[HarnessModel] | None = None,
    ) -> dict | HarnessModel:
        """Perform PUT request with retry.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            body: Request body (BaseModel or dict).
            response_model: Pydantic model for response deserialization.

        Returns:
            Deserialized response or dict if no model provided.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
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
        params: dict | None = None,
        body: HarnessModel | dict | None = None,
        response_model: type[HarnessModel] | None = None,
    ) -> dict | HarnessModel:
        """Perform PATCH request with retry.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            body: Request body (BaseModel or dict).
            response_model: Pydantic model for response deserialization.

        Returns:
            Deserialized response or dict if no model provided.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
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
        params: dict | None = None,
        body: HarnessModel | dict | None = None,
        response_model: type[HarnessModel] | None = None,
    ) -> dict | HarnessModel:
        """Perform DELETE request with retry.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            body: Request body (BaseModel or dict).
            response_model: Pydantic model for response deserialization.

        Returns:
            Deserialized response or dict if no model provided.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
        """

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
        method: str | None = "get",
        body: HarnessModel | dict | None = None,
        params: dict | None = None,
        response_model: type[HarnessModel] | None = None,
        pagination_style: PaginationStyle = PaginationStyle.OFFSET,
        scope: Scope | None = None,
        unwrap_field: str | None = None,
    ) -> Generator[Any, None, None]:
        """Paginate through results using specified pagination style.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            response_model: Pydantic model for individual items.
            pagination_style: OFFSET or CURSOR.
            scope: Optional scope for URL building.
            unwrap_field: Optional field name to extract from each item (e.g., "secret", "connector").

        Yields:
            Individual items from paginated response.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
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

                if method == "post":
                    response = self._post(url, params=params, body=request_body)
                else:
                    response = self._get(url, params=params)

                # Extract items from response - handle multiple response structures:
                # 1. Direct array (pipelines: /v1/orgs/{org}/projects/{project}/pipelines)
                # 2. Nested data.content (connectors/secrets: /ng/api/*)
                if isinstance(response, list):
                    items = response
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

        elif pagination_style == PaginationStyle.TODO:
            # TODO: pagination style unconfirmed — return single page without pagination
            if method == "post":
                response = self._post(url, params=params, body=request_body)
            else:
                response = self._get(url, params=params)

            # Extract items from response - handle multiple response structures
            if isinstance(response, list):
                items = response
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
            else:
                items = []

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

    @property
    def connectors(self):
        """Lazy-loaded ConnectorsApi instance."""
        if not hasattr(self, "_connectors"):
            from harness_python_sdk.ng_api.connectors import ConnectorsApi

            self._connectors = ConnectorsApi(self)
        return self._connectors

    @property
    def secrets(self):
        """Lazy-loaded SecretsApi instance."""
        if not hasattr(self, "_secrets"):
            from harness_python_sdk.ng_api.secrets import SecretsApi

            self._secrets = SecretsApi(self)
        return self._secrets

    @property
    def environments_v2(self):
        """Lazy-loaded InfrastructureApi instance."""
        if not hasattr(self, "_environments_v2"):
            from harness_python_sdk.ng_api.environments_v2 import EnvironmentsV2Api

            self._environments_v2 = EnvironmentsV2Api(self)
        return self._environments_v2

    @property
    def infrastructures(self):
        """Lazy-loaded InfrastructuresApi instance."""
        if not hasattr(self, "_infrastructures"):
            from harness_python_sdk.ng_api.infrastructures import InfrastructuresApi

            self._infrastructures = InfrastructuresApi(self)
        return self._infrastructures

    @property
    def organizations(self):
        """Lazy-loaded OrganizationsApi instance."""
        if not hasattr(self, "_organizations"):
            from harness_python_sdk.ng_api.organizations import OrganizationsApi

            self._organizations = OrganizationsApi(self)
        return self._organizations

    @property
    def projects(self):
        """Lazy-loaded ProjectsApi instance."""
        if not hasattr(self, "_projects"):
            from harness_python_sdk.ng_api.projects import ProjectsApi

            self._projects = ProjectsApi(self)
        return self._projects

    @property
    def services(self):
        """Lazy-loaded ServicesApi instance."""
        if not hasattr(self, "_services"):
            from harness_python_sdk.ng_api.services import ServicesApi

            self._services = ServicesApi(self)
        return self._services

    @property
    def roles(self):
        """Lazy-loaded RolesApi instance."""
        if not hasattr(self, "_roles"):
            from harness_python_sdk.authz.roles import RolesApi

            self._roles = RolesApi(self)
        return self._roles

    @property
    def resource_groups(self):
        """Lazy-loaded ResourceGroupsApi instance."""
        if not hasattr(self, "_resource_groups"):
            from harness_python_sdk.authz.resource_groups import ResourceGroupsApi

            self._resource_groups = ResourceGroupsApi(self)
        return self._resource_groups

    @property
    def role_assignments(self):
        """Lazy-loaded RoleAssignmentsApi instance."""
        if not hasattr(self, "_role_assignments"):
            from harness_python_sdk.authz.role_assignments import RoleAssignmentsApi

            self._role_assignments = RoleAssignmentsApi(self)
        return self._role_assignments

    @property
    def user_groups(self):
        """Lazy-loaded UserGroupsApi instance."""
        if not hasattr(self, "_user_groups"):
            from harness_python_sdk.ng_api.user_groups import UserGroupsApi

            self._user_groups = UserGroupsApi(self)
        return self._user_groups

    @property
    def pipelines_v0(self):
        """Lazy-loaded PipelinesApi instance."""
        if not hasattr(self, "_pipelines_v0"):
            from harness_python_sdk.pipeline_api.pipelines_v0 import PipelinesV0Api

            self._pipelines_v0 = PipelinesV0Api(self)
        return self._pipelines_v0

    @property
    def input_sets_v0(self):
        """Lazy-loaded InputSetsV0Api instance."""
        if not hasattr(self, "_input_sets_v0"):
            from harness_python_sdk.pipeline_api.input_sets_v0 import InputSetsV0Api

            self._input_sets_v0 = InputSetsV0Api(self)
        return self._input_sets_v0

    @property
    def triggers_v0(self):
        """Lazy-loaded TriggersV0Api instance."""
        if not hasattr(self, "_triggers_v0"):
            from harness_python_sdk.pipeline_api.triggers_v0 import TriggersV0Api

            self._triggers_v0 = TriggersV0Api(self)
        return self._triggers_v0

    @property
    def templates_v0(self):
        """Lazy-loaded TemplatesV0Api instance."""
        if not hasattr(self, "_templates_v0"):
            from harness_python_sdk.template_api.templates_v0 import TemplatesV0Api

            self._templates_v0 = TemplatesV0Api(self)
        return self._templates_v0

    @property
    def workspaces(self):
        """Lazy-loaded WorkspacesApi instance."""
        if not hasattr(self, "_workspaces"):
            from harness_python_sdk.iacm_api.workspaces import WorkspacesApi

            self._workspaces = WorkspacesApi(self)
        return self._workspaces

    @property
    def workspace_approvals(self):
        """Lazy-loaded WorkspaceApprovalsApi instance."""
        if not hasattr(self, "_workspace_approvals"):
            from harness_python_sdk.iacm_api.workspace_approvals import WorkspaceApprovalsApi

            self._workspace_approvals = WorkspaceApprovalsApi(self)
        return self._workspace_approvals

    @property
    def workspace_default_pipelines(self):
        """Lazy-loaded WorkspaceDefaultPipelinesApi instance."""
        if not hasattr(self, "_workspace_default_pipelines"):
            from harness_python_sdk.iacm_api.workspace_default_pipelines import WorkspaceDefaultPipelinesApi

            self._workspace_default_pipelines = WorkspaceDefaultPipelinesApi(self)
        return self._workspace_default_pipelines

    @property
    def workspace_states(self):
        """Lazy-loaded WorkspaceStatesApi instance."""
        if not hasattr(self, "_workspace_states"):
            from harness_python_sdk.iacm_api.workspace_states import WorkspaceStatesApi

            self._workspace_states = WorkspaceStatesApi(self)
        return self._workspace_states

    @property
    def workspace_variables(self):
        """Lazy-loaded WorkspaceVariablesApi instance."""
        if not hasattr(self, "_workspace_variables"):
            from harness_python_sdk.iacm_api.workspace_variables import WorkspaceVariablesApi

            self._workspace_variables = WorkspaceVariablesApi(self)
        return self._workspace_variables

    @property
    def variables(self):
        """Lazy-loaded VariablesApi instance."""
        if not hasattr(self, "_variables"):
            from harness_python_sdk.ng_api.variables import VariablesApi

            self._variables = VariablesApi(self)
        return self._variables
