"""
Harness SDK client — main entry point for API interactions.

HarnessClient handles HTTP requests, scope resolution, URL construction,
error handling, and pagination. Supports both context manager and explicit close().
"""

import json
import time
from typing import Any, Callable, Generator, TypeVar

import httpx
import tenacity
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

        if not account_id:
            raise ScopeNotSetError("account_id not set in scope or config")

        return Scope(account_id=account_id, org=org, project=project)

    def _build_url(self, path_template: str, scope: Scope, **kwargs) -> str:
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
            **kwargs,
        }

        # Check for missing placeholders
        import re

        placeholders = set(re.findall(r"\{(\w+)\}", path_template))
        for placeholder in placeholders:
            if subs.get(placeholder) is None:
                raise ScopeNotSetError(f"Missing required placeholder: {placeholder}")

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
            return

        status_code = response.status_code
        body = response.text
        headers = dict(response.headers)

        if status_code in (401, 403):
            raise AuthError(status_code, body, headers)
        else:
            raise ApiError(status_code, body, headers)

    def _should_retry_status_code(self, status_code: int) -> bool:
        """Check if a status code should trigger a retry.

        Args:
            status_code: HTTP status code.

        Returns:
            True if should retry, False otherwise.
        """
        return (
            self._config.retry_enabled
            and status_code in self._config.retry_status_codes
        )

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

            # Raise for non-success responses
            self._raise_for_status(response)
            break

        if response_model:
            return response_model(**response.json())
        return response.json()

    def _post(
        self,
        url: str,
        params: dict | None = None,
        body: HarnessModel | dict | None = None,
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
            response = self._http_client.post(url, params=params, json=request_body)

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

    def _put(
        self,
        url: str,
        params: dict | None = None,
        body: HarnessModel | dict | None = None,
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
            response = self._http_client.put(url, params=params, json=request_body)

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
        response_model: type[HarnessModel] | None = None,
    ) -> dict | HarnessModel:
        """Perform DELETE request with retry.

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
            response = self._http_client.delete(url, params=params)

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

    def _paginate(
        self,
        url: str,
        params: dict | None = None,
        response_model: type[HarnessModel] | None = None,
        pagination_style: PaginationStyle = PaginationStyle.OFFSET,
        scope: Scope | None = None,
    ) -> Generator[Any, None, None]:
        """Paginate through results using specified pagination style.

        Args:
            url: Request URL (relative to base_url).
            params: Query parameters.
            response_model: Pydantic model for individual items.
            pagination_style: OFFSET or CURSOR.
            scope: Optional scope for URL building.

        Yields:
            Individual items from paginated response.

        Raises:
            AuthError: For 401/403.
            ApiError: For other non-2xx.
        """
        if params is None:
            params = {}

        if pagination_style == PaginationStyle.OFFSET:
            # Offset-based pagination (pageIndex/pageSize)
            page_index = params.get("pageIndex", 0)
            page_size = params.get("pageSize", 100)

            while True:
                params["pageIndex"] = page_index
                params["pageSize"] = page_size

                response = self._get(url, params=params)

                # Extract items from response (expect list or dict with items)
                items = response if isinstance(response, list) else response.get("data", [])

                if not items:
                    break

                # Yield each item
                for item in items:
                    if response_model and not isinstance(item, response_model):
                        yield response_model(**item)
                    else:
                        yield item

                # Stop if fewer items than page size
                if len(items) < page_size:
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

                response = self._get(url, params=params)

                # Extract items and next token
                items = response if isinstance(response, list) else response.get("data", [])
                next_token = None
                if isinstance(response, dict):
                    next_token = response.get("pageToken")

                if not items:
                    break

                # Yield each item
                for item in items:
                    if response_model and not isinstance(item, response_model):
                        yield response_model(**item)
                    else:
                        yield item

                if not next_token:
                    break
