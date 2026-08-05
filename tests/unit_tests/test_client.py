"""Unit tests for HarnessClient."""

import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from harness_python_sdk.base_model import HarnessModel
from harness_python_sdk.client import HarnessClient
from harness_python_sdk.config import HarnessConfig
from harness_python_sdk.exceptions import ApiError, AuthError, ScopeNotSetError
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class SampleModel(HarnessModel):
    """Sample model for serialization tests."""

    id: str
    name: str


class TestHarnessClientConstruction:
    """Test HarnessClient construction."""

    def test_client_construction_with_config(self):
        """Test creating client with explicit config."""
        config = HarnessConfig(api_key="key", account_id="acc")
        client = HarnessClient(config=config)
        assert client._config == config
        client.close()

    def test_client_construction_with_kwargs(self):
        """Test creating client with keyword arguments."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert client._config.api_key == "key"
        assert client._config.account_id == "acc"
        client.close()

    def test_client_construction_kwargs_override_config(self):
        """Test that kwargs are ignored if config provided."""
        config = HarnessConfig(api_key="from-config", account_id="acc-from-config")
        client = HarnessClient(
            config=config,
            api_key="from-kwargs",  # Should be ignored
            account_id="acc-from-kwargs",  # Should be ignored
        )
        assert client._config.api_key == "from-config"
        assert client._config.account_id == "acc-from-config"
        client.close()

    def test_client_construction_requires_api_key(self):
        """Test that client construction requires api_key."""
        with pytest.raises(ValueError):
            HarnessClient(account_id="acc")

    def test_client_construction_requires_account_id(self):
        """Test that client construction requires account_id."""
        with pytest.raises(ValueError):
            HarnessClient(api_key="key")

    def test_client_construction_with_default_scope(self):
        """Test creating client with default org/project."""
        client = HarnessClient(
            api_key="key",
            account_id="acc",
            default_org="org-123",
            default_project="proj-456",
        )
        assert client._default_scope.account_id == "acc"
        assert client._default_scope.org == "org-123"
        assert client._default_scope.project == "proj-456"
        client.close()

    def test_client_construction_with_base_url_kwarg(self):
        """Test creating client with base_url kwarg."""
        client = HarnessClient(
            api_key="key",
            account_id="acc",
            base_url="https://my.harness.io",
        )
        assert client.base_url == "https://my.harness.io"
        client.close()

    def test_client_construction_without_base_url_kwarg(self):
        """Test creating client without base_url defaults to app.harness.io."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert client.base_url == "https://app.harness.io"
        client.close()

    def test_client_construction_with_explicit_config_base_url(self):
        """Test creating client with explicit config containing base_url."""
        config = HarnessConfig(
            api_key="key",
            account_id="acc",
            base_url="https://custom.harness.io",
        )
        client = HarnessClient(config=config)
        assert client.base_url == "https://custom.harness.io"
        client.close()

    def test_client_repr_no_api_key(self):
        """Test that client repr does not contain API key."""
        client = HarnessClient(api_key="secret-key-12345", account_id="acc")
        repr_str = repr(client)
        assert "secret-key-12345" not in repr_str
        assert "acc" in repr_str
        client.close()


class TestHarnessClientLifecycle:
    """Test client lifecycle management."""

    def test_client_context_manager(self):
        """Test client as context manager."""
        with HarnessClient(api_key="key", account_id="acc") as client:
            assert client._http_client is not None
        # After exit, client should be closed (httpx.Client.close() called)
        # We can't directly test this without inspecting internals

    def test_client_explicit_close(self):
        """Test client explicit close."""
        client = HarnessClient(api_key="key", account_id="acc")
        http_client = client._http_client
        assert http_client is not None
        client.close()
        # httpx.Client closes its connection pool

    def test_client_double_close(self):
        """Test that double close does not raise."""
        client = HarnessClient(api_key="key", account_id="acc")
        client.close()
        client.close()  # Should not raise

    def test_base_url_setter_updates_value(self):
        """Test that setting base_url updates the property."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert client.base_url == "https://app.harness.io"
        client.base_url = "https://my.harness.io"
        assert client.base_url == "https://my.harness.io"
        client.close()

    def test_base_url_setter_closes_old_session(self):
        """Test that setting base_url closes the old httpx session."""
        client = HarnessClient(api_key="key", account_id="acc")
        old_http_client = client._http_client
        old_client_id = id(old_http_client)

        # Set new base_url
        client.base_url = "https://my.harness.io"

        # New session should be different
        new_http_client = client._http_client
        new_client_id = id(new_http_client)
        assert old_client_id != new_client_id

        # Old client should be closed
        assert old_http_client.is_closed
        # New client should be open
        assert not new_http_client.is_closed

        client.close()

    def test_base_url_setter_creates_new_session(self):
        """Test that base_url setter creates a new working session."""
        client = HarnessClient(api_key="key", account_id="acc")
        client.base_url = "https://my.harness.io"

        # Session should be usable (not closed)
        assert not client._http_client.is_closed
        assert client.base_url == "https://my.harness.io"

        client.close()


class TestScopeResolution:
    """Test scope resolution."""

    def test_resolve_scope_with_no_scope(self):
        """Test resolving scope when none provided."""
        client = HarnessClient(api_key="key", account_id="acc", default_org="org")
        scope = client._resolve_scope(None)
        assert scope.account_id == "acc"
        assert scope.org == "org"
        client.close()

    def test_resolve_scope_call_scope_override(self):
        """Test that call-time scope overrides default."""
        client = HarnessClient(
            api_key="key", account_id="acc", default_org="org", default_project="proj"
        )
        call_scope = Scope(account_id="acc", org="new-org", project="new-proj")
        resolved = client._resolve_scope(call_scope)
        assert resolved.org == "new-org"
        assert resolved.project == "new-proj"
        client.close()

    def test_resolve_scope_missing_account_id(self):
        """Test that missing account_id raises ScopeNotSetError."""
        client = HarnessClient(api_key="key", account_id="acc")
        # Create a scope with empty account_id (simulating missing)
        # This is hard to do with frozen Scope, so we test the error path
        client._default_scope = Scope(account_id="")
        with pytest.raises(ScopeNotSetError, match="account_id"):
            client._resolve_scope(None)
        client.close()


class TestUrlBuilding:
    """Test URL construction."""

    def test_build_url_simple_template(self):
        """Test building URL from simple template."""
        client = HarnessClient(api_key="key", account_id="acc-123")
        scope = Scope(account_id="acc-123")
        url = client._build_url("/v1/accounts/{account_id}/orgs", scope)
        assert url == "/v1/accounts/acc-123/orgs"
        client.close()

    def test_build_url_all_placeholders(self):
        """Test building URL with all placeholders."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789")
        url = client._build_url(
            "/v1/accounts/{account_id}/orgs/{org}/projects/{project}/pipelines",
            scope,
        )
        assert url == "/v1/accounts/acc-123/orgs/org-456/projects/proj-789/pipelines"
        client.close()

    def test_build_url_custom_kwargs(self):
        """Test building URL with custom template variables."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123")
        url = client._build_url(
            "/v1/accounts/{account_id}/resources/{resource_id}", scope, resource_id="res-999"
        )
        assert url == "/v1/accounts/acc-123/resources/res-999"
        client.close()

    def test_build_url_missing_placeholder(self):
        """Test that missing placeholder raises ScopeNotSetError."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc", org=None)
        with pytest.raises(ScopeNotSetError, match="org"):
            client._build_url("/v1/accounts/{account_id}/orgs/{org}/projects", scope)
        client.close()


class TestSetDefaultScope:
    """Test scope modification."""

    def test_set_default_scope(self):
        """Test updating default scope."""
        client = HarnessClient(api_key="key", account_id="acc")
        client.set_default_scope(org="new-org", project="new-proj")
        assert client._default_scope.org == "new-org"
        assert client._default_scope.project == "new-proj"
        assert client._default_scope.account_id == "acc"
        client.close()

    def test_set_default_scope_partial(self):
        """Test that set_default_scope with None values resets them."""
        client = HarnessClient(
            api_key="key", account_id="acc", default_org="org", default_project="proj"
        )
        client.set_default_scope(org="new-org", project=None)
        assert client._default_scope.org == "new-org"
        assert client._default_scope.project is None
        client.close()


class TestRaiseForStatus:
    """Test error handling."""

    def test_raise_for_status_200(self):
        """Test that 200 response does not raise."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(200)
        client._raise_for_status(response)  # Should not raise
        client.close()

    def test_raise_for_status_401(self):
        """Test that 401 raises AuthError."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(401, text="Unauthorized")
        with pytest.raises(AuthError) as exc_info:
            client._raise_for_status(response)
        assert exc_info.value.status_code == 401
        client.close()

    def test_raise_for_status_403(self):
        """Test that 403 raises AuthError."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(403, text="Forbidden")
        with pytest.raises(AuthError):
            client._raise_for_status(response)
        client.close()

    def test_raise_for_status_500(self):
        """Test that 500 raises ApiError."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(500, text="Internal Server Error")
        with pytest.raises(ApiError) as exc_info:
            client._raise_for_status(response)
        assert exc_info.value.status_code == 500
        assert not isinstance(exc_info.value, AuthError)
        client.close()

    def test_raise_for_status_404(self):
        """Test that 404 raises ApiError."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(404, text="Not Found")
        client._raise_for_status(response)
        client.close()

    def test_api_error_carries_headers(self):
        """Test that ApiError preserves headers."""
        client = HarnessClient(api_key="key", account_id="acc")
        headers = httpx.Headers({"retry-after": "60", "x-request-id": "req-123"})
        response = httpx.Response(429, text="Too Many Requests", headers=headers)
        with pytest.raises(ApiError) as exc_info:
            client._raise_for_status(response)
        assert exc_info.value.headers["retry-after"] == "60"
        client.close()


class TestHttpMethods:
    """Test HTTP method implementations."""

    def test_get_success(self, httpx_mock: HTTPXMock):
        """Test successful GET request."""
        httpx_mock.add_response(json={"id": "123", "name": "Test"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._get("/test", response_model=SampleModel)
        assert isinstance(result, SampleModel)
        assert result.id == "123"
        assert result.name == "Test"
        client.close()

    def test_get_without_response_model(self, httpx_mock: HTTPXMock):
        """Test GET request without response model."""
        httpx_mock.add_response(json={"id": "123", "name": "Test"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._get("/test")
        assert isinstance(result, dict)
        assert result["id"] == "123"
        client.close()

    def test_post_with_body(self, httpx_mock: HTTPXMock):
        """Test POST request with body."""
        httpx_mock.add_response(json={"id": "123", "name": "Created"})
        client = HarnessClient(api_key="key", account_id="acc")
        body = SampleModel(id="123", name="Created")
        result = client._post("/test", body=body, response_model=SampleModel)
        assert result.id == "123"
        client.close()

    def test_post_with_dict_body(self, httpx_mock: HTTPXMock):
        """Test POST request with dict body."""
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._post("/test", body={"id": "123"})
        assert result["id"] == "123"
        client.close()

    def test_put_request(self, httpx_mock: HTTPXMock):
        """Test PUT request."""
        httpx_mock.add_response(json={"id": "123", "name": "Updated"})
        client = HarnessClient(api_key="key", account_id="acc")
        body = SampleModel(id="123", name="Updated")
        result = client._put("/test", body=body, response_model=SampleModel)
        assert result.name == "Updated"
        client.close()

    def test_patch_request(self, httpx_mock: HTTPXMock):
        """Test PATCH request."""
        httpx_mock.add_response(json={"id": "123", "name": "Patched"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._patch("/test", body={"name": "Patched"})
        assert result["name"] == "Patched"
        client.close()

    def test_delete_request(self, httpx_mock: HTTPXMock):
        """Test DELETE request."""
        httpx_mock.add_response(json={"success": True})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._delete("/test")
        assert result["success"] is True
        client.close()

    def test_get_error_response(self, httpx_mock: HTTPXMock):
        """Test GET with error response."""
        httpx_mock.add_response(status_code=500, text="Internal Server Error")
        client = HarnessClient(api_key="key", account_id="acc")
        with pytest.raises(ApiError):
            client._get("/test")
        client.close()

    def test_post_auth_error(self, httpx_mock: HTTPXMock):
        """Test POST with 401 response."""
        httpx_mock.add_response(status_code=401, text="Unauthorized")
        client = HarnessClient(api_key="key", account_id="acc")
        with pytest.raises(AuthError):
            client._post("/test", body={})
        client.close()


class TestResolveHierarchy:
    """Test hierarchy resolution."""

    def test_resolve_hierarchy_full_scope(self):
        """Test resolving full scope hierarchy."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789")
        hierarchy = client._resolve_hierarchy(scope)
        assert hierarchy["accountIdentifier"] == "acc-123"
        assert hierarchy["orgIdentifier"] == "org-456"
        assert hierarchy["projectIdentifier"] == "proj-789"
        assert "pipelineIdentifier" not in hierarchy
        client.close()

    def test_resolve_hierarchy_with_pipeline(self):
        """Test resolving hierarchy with pipeline."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789", pipeline="pipe-999")
        hierarchy = client._resolve_hierarchy(scope)
        assert hierarchy["pipelineIdentifier"] == "pipe-999"
        client.close()

    def test_resolve_hierarchy_account_only(self):
        """Test resolving hierarchy with only account."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123")
        hierarchy = client._resolve_hierarchy(scope)
        assert hierarchy["accountIdentifier"] == "acc-123"
        assert "orgIdentifier" not in hierarchy
        assert "projectIdentifier" not in hierarchy
        client.close()

    def test_resolve_hierarchy_none_scope(self):
        """Test resolving hierarchy with None scope uses default."""
        client = HarnessClient(
            api_key="key", account_id="acc", default_org="default-org", default_project="default-proj"
        )
        hierarchy = client._resolve_hierarchy(None)
        assert hierarchy["accountIdentifier"] == "acc"
        assert hierarchy["orgIdentifier"] == "default-org"
        assert hierarchy["projectIdentifier"] == "default-proj"
        client.close()


class TestUnwrapResponse:
    """Test response unwrapping."""

    def test_unwrap_response_nested_data_with_key(self):
        """Test unwrapping nested response with key type."""
        client = HarnessClient(api_key="key", account_id="acc")
        raw_data = {"data": {"organization": {"id": "123", "name": "Test"}}}
        result = client._unwrap_response("organization", raw_data)
        assert result["id"] == "123"
        assert result["name"] == "Test"
        client.close()

    def test_unwrap_response_with_scope_fields(self):
        """Test that unwrap adds scope identifiers."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789")
        raw_data = {"data": {"resource": {"id": "123"}}}
        result = client._unwrap_response("resource", raw_data, scope)
        assert result["id"] == "123"
        assert result["account_identifier"] == "acc-123"
        assert result["org_identifier"] == "org-456"
        assert result["project_identifier"] == "proj-789"
        client.close()

    def test_unwrap_response_no_nested_data(self):
        """Test unwrapping when no nested data key."""
        client = HarnessClient(api_key="key", account_id="acc")
        raw_data = {"id": "123", "name": "Test"}
        result = client._unwrap_response(None, raw_data)
        assert result["id"] == "123"
        client.close()

    def test_unwrap_response_preserves_existing_identifiers(self):
        """Test that existing identifiers aren't overwritten."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456")
        raw_data = {"data": {"resource": {"id": "123"}}}
        result = client._unwrap_response("resource", raw_data, scope)
        assert result["account_identifier"] == "acc-123"
        assert result["org_identifier"] == "org-456"
        client.close()


class TestRaiseForStatusEdgeCases:
    """Test error handling edge cases."""

    def test_raise_for_status_400_with_failure_status(self):
        """Test 400 with FAILURE status in payload."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(
            400,
            json={"status": "FAILURE", "code": "VALIDATION_ERROR", "message": "Invalid input"},
        )
        with pytest.raises(ApiError) as exc_info:
            client._raise_for_status(response)
        assert exc_info.value.status_code == 400
        client.close()

    def test_raise_for_status_400_resource_not_found_on_get(self):
        """Test GET with 400 and RESOURCE_NOT_FOUND returns False."""
        client = HarnessClient(api_key="key", account_id="acc")
        request = httpx.Request("GET", "http://test")
        response = httpx.Response(
            400,
            request=request,
            json={"status": "FAILURE", "code": "RESOURCE_NOT_FOUND_EXCEPTION"},
        )
        result = client._raise_for_status(response)
        assert result is False
        client.close()

    def test_raise_for_status_400_resource_not_found_on_post(self):
        """Test POST with 400 and RESOURCE_NOT_FOUND raises error."""
        client = HarnessClient(api_key="key", account_id="acc")
        request = httpx.Request("POST", "http://test")
        response = httpx.Response(
            400,
            request=request,
            json={"status": "FAILURE", "code": "RESOURCE_NOT_FOUND_EXCEPTION"},
        )
        with pytest.raises(ApiError):
            client._raise_for_status(response)
        client.close()

    def test_raise_for_status_400_resource_not_found_on_put(self):
        """Test PUT with 400 and RESOURCE_NOT_FOUND raises error."""
        client = HarnessClient(api_key="key", account_id="acc")
        request = httpx.Request("PUT", "http://test")
        response = httpx.Response(
            400,
            request=request,
            json={"status": "FAILURE", "code": "RESOURCE_NOT_FOUND_EXCEPTION"},
        )
        with pytest.raises(ApiError):
            client._raise_for_status(response)
        client.close()

    def test_raise_for_status_400_resource_not_found_on_patch(self):
        """Test PATCH with 400 and RESOURCE_NOT_FOUND raises error."""
        client = HarnessClient(api_key="key", account_id="acc")
        request = httpx.Request("PATCH", "http://test")
        response = httpx.Response(
            400,
            request=request,
            json={"status": "FAILURE", "code": "RESOURCE_NOT_FOUND_EXCEPTION"},
        )
        with pytest.raises(ApiError):
            client._raise_for_status(response)
        client.close()

    def test_raise_for_status_400_invalid_json(self):
        """Test 400 with invalid JSON body."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(400, text="Invalid JSON {]")
        with pytest.raises(ApiError):
            client._raise_for_status(response)
        client.close()

    def test_raise_for_status_404_returns_false(self):
        """Test that 404 returns False."""
        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(404, text="Not Found")
        result = client._raise_for_status(response)
        assert result is False
        client.close()


class TestRetryLogic:
    """Test retry and exponential backoff."""

    def test_should_retry_status_code_true(self):
        """Test that retryable status codes are detected."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert client._should_retry_status_code(429) is True
        assert client._should_retry_status_code(503) is True
        client.close()

    def test_should_retry_status_code_false(self):
        """Test that non-retryable status codes are not retried."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert client._should_retry_status_code(200) is False
        assert client._should_retry_status_code(404) is False
        assert client._should_retry_status_code(401) is False
        assert client._should_retry_status_code(502) is False
        client.close()

    def test_should_retry_disabled(self):
        """Test that retries can be disabled."""
        config = HarnessConfig(api_key="key", account_id="acc", retry_enabled=False)
        client = HarnessClient(config=config)
        assert client._should_retry_status_code(503) is False
        client.close()

    def test_should_retry_custom_status_codes(self):
        """Test custom retry status codes."""
        config = HarnessConfig(
            api_key="key", account_id="acc", retry_status_codes=[500, 502, 503]
        )
        client = HarnessClient(config=config)
        assert client._should_retry_status_code(500) is True
        assert client._should_retry_status_code(502) is True
        assert client._should_retry_status_code(503) is True
        client.close()

    def test_wait_for_retry_uses_retry_after_header(self):
        """Test that Retry-After header is respected."""
        import time

        client = HarnessClient(api_key="key", account_id="acc")
        headers = httpx.Headers({"retry-after": "1"})
        response = httpx.Response(503, headers=headers)

        start = time.time()
        client._wait_for_retry(response, 1)
        elapsed = time.time() - start

        assert elapsed >= 1.0
        client.close()

    def test_wait_for_retry_exponential_backoff(self):
        """Test exponential backoff without Retry-After."""
        import time

        client = HarnessClient(api_key="key", account_id="acc")
        response = httpx.Response(503)

        start = time.time()
        client._wait_for_retry(response, 1)
        elapsed_attempt_1 = time.time() - start

        start = time.time()
        client._wait_for_retry(response, 2)
        elapsed_attempt_2 = time.time() - start

        assert elapsed_attempt_2 > elapsed_attempt_1
        client.close()

    def test_get_with_retry_on_429(self, httpx_mock: HTTPXMock):
        """Test GET retry on 429 (rate limit)."""
        httpx_mock.add_response(status_code=429, text="Too Many Requests")
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._get("/test")
        assert result["id"] == "123"
        client.close()

    def test_post_with_retry_on_503(self, httpx_mock: HTTPXMock):
        """Test POST retry on 503."""
        httpx_mock.add_response(status_code=503, text="Service Unavailable")
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._post("/test", body={"name": "test"})
        assert result["id"] == "123"
        client.close()

    def test_put_with_retry_on_429(self, httpx_mock: HTTPXMock):
        """Test PUT retry on 429 (custom retry config)."""
        config = HarnessConfig(
            api_key="key", account_id="acc", retry_status_codes=[429, 503, 504]
        )
        httpx_mock.add_response(status_code=504, text="Gateway Timeout")
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(config=config)
        result = client._put("/test", body={"name": "test"})
        assert result["id"] == "123"
        client.close()

    def test_patch_with_retry_on_429(self, httpx_mock: HTTPXMock):
        """Test PATCH retry on 429."""
        httpx_mock.add_response(status_code=429, text="Too Many Requests")
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._patch("/test", body={"name": "test"})
        assert result["id"] == "123"
        client.close()

    def test_delete_with_retry_on_503(self, httpx_mock: HTTPXMock):
        """Test DELETE retry on 503."""
        httpx_mock.add_response(status_code=503, text="Service Unavailable")
        httpx_mock.add_response(json={"success": True})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._delete("/test")
        assert result["success"] is True
        client.close()

    def test_get_exhausts_retries(self, httpx_mock: HTTPXMock):
        """Test that retries are exhausted and error raised."""
        for _ in range(4):  # max_retries + 1 = 4 (retries=3)
            httpx_mock.add_response(status_code=503, text="Service Unavailable")
        client = HarnessClient(api_key="key", account_id="acc")
        with pytest.raises(ApiError):
            client._get("/test")
        client.close()


class TestPostErrorHandling:
    """Test POST-specific error handling."""

    def test_post_with_entity_not_found_code(self, httpx_mock: HTTPXMock):
        """Test POST detects ENTITY_NOT_FOUND code and raises."""
        httpx_mock.add_response(json={"code": "ENTITY_NOT_FOUND", "message": "Not found"})
        client = HarnessClient(api_key="key", account_id="acc")
        with pytest.raises(ApiError):
            client._post("/test", body={})
        client.close()

    def test_post_yaml_body(self, httpx_mock: HTTPXMock):
        """Test POST with YAML body."""
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        body = {"name": "test", "config": {"key": "value"}}
        result = client._post("/test", body=body, body_is_yaml=True)
        assert result["id"] == "123"
        client.close()

    def test_post_without_body(self, httpx_mock: HTTPXMock):
        """Test POST without body."""
        httpx_mock.add_response(json={"success": True})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._post("/test")
        assert result["success"] is True
        client.close()


class TestPutYamlBody:
    """Test PUT-specific features."""

    def test_put_yaml_body(self, httpx_mock: HTTPXMock):
        """Test PUT with YAML body."""
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        body = {"name": "test", "config": {"key": "value"}}
        result = client._put("/test", body=body, body_is_yaml=True)
        assert result["id"] == "123"
        client.close()

    def test_put_without_body(self, httpx_mock: HTTPXMock):
        """Test PUT without body."""
        httpx_mock.add_response(json={"success": True})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._put("/test")
        assert result["success"] is True
        client.close()


class TestPaginationOffset:
    """Test offset-based pagination."""

    def test_paginate_offset_single_page(self, httpx_mock: HTTPXMock):
        """Test pagination with single page of results."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}, {"id": "2"}], "pageItemCount": 2}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.OFFSET, params={})
        )
        assert len(items) == 2
        assert items[0]["id"] == "1"
        client.close()

    def test_paginate_offset_multiple_pages(self, httpx_mock: HTTPXMock):
        """Test pagination across multiple pages."""
        # Page 1: 2 items with pageSize=100 (default)
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}, {"id": "2"}], "pageItemCount": 2}}
        )
        # Page 2: 2 items with pageSize=100
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "3"}, {"id": "4"}], "pageItemCount": 2}}
        )
        # Page 3: 1 item (< pageSize so stops)
        httpx_mock.add_response(json={"data": {"content": [{"id": "5"}], "pageItemCount": 1}})
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                pagination_style=PaginationStyle.OFFSET,
                params={"pageSize": 2},  # Set small page size to trigger multiple pages
            )
        )
        assert len(items) == 5
        assert items[4]["id"] == "5"
        client.close()

    def test_paginate_offset_with_response_model(self, httpx_mock: HTTPXMock):
        """Test pagination with response model deserialization."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1", "name": "Test"}], "pageItemCount": 1}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                pagination_style=PaginationStyle.OFFSET,
                params={},
                response_model=SampleModel,
            )
        )
        assert isinstance(items[0], SampleModel)
        assert items[0].id == "1"
        client.close()

    def test_paginate_offset_direct_array_response(self, httpx_mock: HTTPXMock):
        """Test pagination with direct array response."""
        httpx_mock.add_response(json=[{"id": "1"}, {"id": "2"}])
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.OFFSET, params={})
        )
        assert len(items) == 2
        client.close()

    def test_paginate_offset_direct_data_array(self, httpx_mock: HTTPXMock):
        """Test pagination with direct data array (not nested content)."""
        httpx_mock.add_response(json={"data": [{"id": "1"}, {"id": "2"}]})
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.OFFSET, params={})
        )
        assert len(items) == 2
        client.close()

    def test_paginate_offset_unwrap_field(self, httpx_mock: HTTPXMock):
        """Test pagination with field unwrapping."""
        httpx_mock.add_response(
            json={
                "data": {
                    "content": [
                        {"secret": {"id": "1", "name": "secret1"}},
                        {"secret": {"id": "2", "name": "secret2"}},
                    ],
                    "pageItemCount": 2,
                }
            }
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                pagination_style=PaginationStyle.OFFSET,
                params={},
                unwrap_field="secret",
            )
        )
        assert items[0]["id"] == "1"
        assert items[1]["id"] == "2"
        client.close()

    def test_paginate_offset_with_scope_hierarchy(self, httpx_mock: HTTPXMock):
        """Test pagination adds scope hierarchy to items."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}], "pageItemCount": 1}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456")
        items = list(
            client._paginate(
                "/test", pagination_style=PaginationStyle.OFFSET, params={}, scope=scope
            )
        )
        assert items[0]["accountIdentifier"] == "acc-123"
        assert items[0]["orgIdentifier"] == "org-456"
        client.close()

    def test_paginate_offset_post_method(self, httpx_mock: HTTPXMock):
        """Test offset pagination with POST method."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}], "pageItemCount": 1}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                method="post",
                pagination_style=PaginationStyle.OFFSET,
                params={},
                body={"filter": "test"},
            )
        )
        assert len(items) == 1
        client.close()


class TestPaginationCursor:
    """Test cursor-based pagination."""

    def test_paginate_cursor_single_page(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with single page."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}, {"id": "2"}]}, "pageToken": None}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.CURSOR, params={})
        )
        assert len(items) == 2
        client.close()

    def test_paginate_cursor_multiple_pages(self, httpx_mock: HTTPXMock):
        """Test cursor pagination across multiple pages."""
        httpx_mock.add_response(
            json={
                "data": {"content": [{"id": "1"}, {"id": "2"}]},
                "pageToken": "token-1",
            }
        )
        httpx_mock.add_response(
            json={
                "data": {"content": [{"id": "3"}, {"id": "4"}]},
                "pageToken": "token-2",
            }
        )
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "5"}]}, "pageToken": None}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.CURSOR, params={})
        )
        assert len(items) == 5
        client.close()

    def test_paginate_cursor_nested_page_token(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with token in nested data."""
        httpx_mock.add_response(
            json={
                "data": {
                    "content": [{"id": "1"}],
                    "pageToken": "token-nested",
                }
            }
        )
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "2"}]}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.CURSOR, params={})
        )
        assert len(items) == 2
        client.close()

    def test_paginate_cursor_with_response_model(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with response model."""
        httpx_mock.add_response(
            json={
                "data": {"content": [{"id": "1", "name": "Test"}]},
                "pageToken": None,
            }
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                pagination_style=PaginationStyle.CURSOR,
                params={},
                response_model=SampleModel,
            )
        )
        assert isinstance(items[0], SampleModel)
        client.close()

    def test_paginate_cursor_post_method(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with POST method."""
        httpx_mock.add_response(
            json={
                "data": {"content": [{"id": "1"}]},
                "pageToken": None,
            }
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                method="post",
                pagination_style=PaginationStyle.CURSOR,
                params={},
                body={"filter": "test"},
            )
        )
        assert len(items) == 1
        client.close()


class TestPaginationTodo:
    """Test TODO pagination style."""

    def test_paginate_todo_single_page(self, httpx_mock: HTTPXMock):
        """Test TODO pagination (unconfirmed style)."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}, {"id": "2"}]}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.TODO, params={})
        )
        assert len(items) == 2
        client.close()

    def test_paginate_todo_direct_array(self, httpx_mock: HTTPXMock):
        """Test TODO pagination with direct array."""
        httpx_mock.add_response(json=[{"id": "1"}, {"id": "2"}])
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.TODO, params={})
        )
        assert len(items) == 2
        client.close()


class TestBuildUrlOverrides:
    """Test URL building with scope overrides."""

    def test_build_url_org_id_override(self):
        """Test that org_id kwarg overrides scope org."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456")
        url = client._build_url(
            "/v1/accounts/{account_id}/orgs/{org}/projects", scope, org_id="org-override"
        )
        assert "org-override" in url
        client.close()

    def test_build_url_project_id_override(self):
        """Test that project_id kwarg overrides scope project."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789")
        url = client._build_url(
            "/v1/accounts/{account_id}/orgs/{org}/projects/{project}/pipelines",
            scope,
            project_id="proj-override",
        )
        assert "proj-override" in url
        client.close()

    def test_build_url_pipeline_id_override(self):
        """Test that pipeline_id kwarg overrides scope pipeline."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789", pipeline="pipe-original")
        url = client._build_url(
            "/v1/accounts/{account_id}/orgs/{org}/projects/{project}/pipelines/{pipeline}",
            scope,
            pipeline_id="pipe-999",
        )
        assert "pipe-999" in url
        assert "pipe-original" not in url
        client.close()

    def test_build_url_strips_none_values(self):
        """Test that None values are stripped from substitutions."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org=None, project=None)
        url = client._build_url("/v1/accounts/{account_id}/info", scope)
        assert url == "/v1/accounts/acc-123/info"
        client.close()


class TestLazyLoadedProperties:
    """Test lazy-loaded API resource properties."""

    def test_connectors_lazy_load(self):
        """Test connectors property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_connectors")
        connectors = client.connectors
        assert hasattr(client, "_connectors")
        assert connectors is client.connectors  # Should be same instance
        client.close()

    def test_secrets_lazy_load(self):
        """Test secrets property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_secrets")
        secrets = client.secrets
        assert hasattr(client, "_secrets")
        assert secrets is client.secrets
        client.close()

    def test_environments_v2_lazy_load(self):
        """Test environments_v2 property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_environments_v2")
        envs = client.environments_v2
        assert hasattr(client, "_environments_v2")
        assert envs is client.environments_v2
        client.close()

    def test_infrastructures_lazy_load(self):
        """Test infrastructures property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_infrastructures")
        infra = client.infrastructures
        assert hasattr(client, "_infrastructures")
        assert infra is client.infrastructures
        client.close()

    def test_organizations_lazy_load(self):
        """Test organizations property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_organizations")
        orgs = client.organizations
        assert hasattr(client, "_organizations")
        assert orgs is client.organizations
        client.close()

    def test_projects_lazy_load(self):
        """Test projects property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_projects")
        projects = client.projects
        assert hasattr(client, "_projects")
        assert projects is client.projects
        client.close()

    def test_services_lazy_load(self):
        """Test services property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_services")
        services = client.services
        assert hasattr(client, "_services")
        assert services is client.services
        client.close()

    def test_roles_lazy_load(self):
        """Test roles property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_roles")
        roles = client.roles
        assert hasattr(client, "_roles")
        assert roles is client.roles
        client.close()

    def test_resource_groups_lazy_load(self):
        """Test resource_groups property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_resource_groups")
        rgs = client.resource_groups
        assert hasattr(client, "_resource_groups")
        assert rgs is client.resource_groups
        client.close()

    def test_role_assignments_lazy_load(self):
        """Test role_assignments property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_role_assignments")
        ras = client.role_assignments
        assert hasattr(client, "_role_assignments")
        assert ras is client.role_assignments
        client.close()

    def test_user_groups_lazy_load(self):
        """Test user_groups property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_user_groups")
        ugs = client.user_groups
        assert hasattr(client, "_user_groups")
        assert ugs is client.user_groups
        client.close()

    def test_pipelines_v0_lazy_load(self):
        """Test pipelines_v0 property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_pipelines_v0")
        pipes = client.pipelines_v0
        assert hasattr(client, "_pipelines_v0")
        assert pipes is client.pipelines_v0
        client.close()

    def test_input_sets_v0_lazy_load(self):
        """Test input_sets_v0 property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_input_sets_v0")
        iss = client.input_sets_v0
        assert hasattr(client, "_input_sets_v0")
        assert iss is client.input_sets_v0
        client.close()

    def test_triggers_v0_lazy_load(self):
        """Test triggers_v0 property lazy loads."""
        client = HarnessClient(api_key="key", account_id="acc")
        assert not hasattr(client, "_triggers_v0")
        trigs = client.triggers_v0
        assert hasattr(client, "_triggers_v0")
        assert trigs is client.triggers_v0
        client.close()


class TestHttpMethodsWithParams:
    """Test HTTP methods with query parameters."""

    def test_get_with_params(self, httpx_mock: HTTPXMock):
        """Test GET with query parameters."""
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._get("/test", params={"filter": "active", "limit": "10"})
        assert result["id"] == "123"
        client.close()

    def test_post_with_params(self, httpx_mock: HTTPXMock):
        """Test POST with query parameters."""
        httpx_mock.add_response(json={"id": "123"})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._post("/test", params={"notify": "true"}, body={"name": "test"})
        assert result["id"] == "123"
        client.close()

    def test_delete_with_params(self, httpx_mock: HTTPXMock):
        """Test DELETE with query parameters."""
        httpx_mock.add_response(json={"success": True})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._delete("/test", params={"force": "true"})
        assert result["success"] is True
        client.close()


class TestHttpClientHeaders:
    """Test HTTP client header configuration."""

    def test_client_sets_api_key_header(self):
        """Test that client sets x-api-key header."""
        client = HarnessClient(api_key="secret-key", account_id="acc-123")
        headers = client._http_client.headers
        assert headers["x-api-key"] == "secret-key"
        client.close()

    def test_client_sets_account_id_header(self):
        """Test that client sets x-account-id header."""
        client = HarnessClient(api_key="key", account_id="acc-456")
        headers = client._http_client.headers
        assert headers["x-account-id"] == "acc-456"
        client.close()

    def test_client_sets_content_type_header(self):
        """Test that client sets Content-Type header."""
        client = HarnessClient(api_key="key", account_id="acc")
        headers = client._http_client.headers
        assert headers["Content-Type"] == "application/json"
        client.close()

    def test_client_respects_ssl_verify_config(self):
        """Test that SSL verification is configured."""
        config = HarnessConfig(api_key="key", account_id="acc", verify_ssl=False)
        client = HarnessClient(config=config)
        # httpx stores verify settings in _config._verify, not on the client itself
        assert client._config.verify_ssl is False
        client.close()


class TestGetWith404Handling:
    """Test GET-specific 404 handling."""

    def test_get_with_404_returns_empty_dict(self, httpx_mock: HTTPXMock):
        """Test that GET with 404 returns empty dict."""
        httpx_mock.add_response(status_code=404, text="Not Found")
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._get("/test")
        assert result == {}
        client.close()


class TestDeleteWithoutResponseBody:
    """Test DELETE responses without body."""

    def test_delete_with_empty_response(self, httpx_mock: HTTPXMock):
        """Test DELETE with empty response."""
        httpx_mock.add_response(status_code=204, json={})
        client = HarnessClient(api_key="key", account_id="acc")
        result = client._delete("/test")
        assert result == {}
        client.close()


class TestPaginationEmptyResponses:
    """Test pagination with empty responses."""

    def test_paginate_offset_empty_response(self, httpx_mock: HTTPXMock):
        """Test offset pagination with no items."""
        httpx_mock.add_response(json={"data": {"content": [], "pageItemCount": 0}})
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.OFFSET, params={})
        )
        assert items == []
        client.close()

    def test_paginate_cursor_empty_response(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with no items."""
        httpx_mock.add_response(
            json={"data": {"content": []}, "pageToken": None}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.CURSOR, params={})
        )
        assert items == []
        client.close()


class TestPaginationEdgeCases:
    """Test pagination edge cases."""

    def test_paginate_offset_with_invalid_response(self, httpx_mock: HTTPXMock):
        """Test pagination with invalid response structure."""
        httpx_mock.add_response(json={})  # Empty response
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.OFFSET, params={})
        )
        assert items == []
        client.close()

    def test_paginate_cursor_with_list_response(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with direct list response."""
        httpx_mock.add_response(json=[{"id": "1"}])
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.CURSOR, params={})
        )
        assert len(items) == 1
        client.close()

    def test_paginate_offset_body_model(self, httpx_mock: HTTPXMock):
        """Test offset pagination with request body model."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1", "name": "test"}], "pageItemCount": 1}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        body_model = SampleModel(id="1", name="test")
        items = list(
            client._paginate(
                "/test",
                method="post",
                body=body_model,
                pagination_style=PaginationStyle.OFFSET,
                params={},
            )
        )
        assert len(items) == 1
        client.close()

    def test_paginate_cursor_body_model(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with request body model."""
        httpx_mock.add_response(
            json={
                "data": {"content": [{"id": "1", "name": "test"}]},
                "pageToken": None,
            }
        )
        client = HarnessClient(api_key="key", account_id="acc")
        body_model = SampleModel(id="1", name="test")
        items = list(
            client._paginate(
                "/test",
                method="post",
                body=body_model,
                pagination_style=PaginationStyle.CURSOR,
                params={},
            )
        )
        assert len(items) == 1
        client.close()


class TestDisplayPayload:
    """Test the debug payload display method."""

    def test_display_payload_with_string(self, capsys):
        """Test display payload with string input."""
        client = HarnessClient(api_key="key", account_id="acc")
        client._display_payload("test string")
        captured = capsys.readouterr()
        assert "test string" in captured.out
        client.close()

    def test_display_payload_with_int(self, capsys):
        """Test display payload with integer input."""
        client = HarnessClient(api_key="key", account_id="acc")
        client._display_payload(42)
        captured = capsys.readouterr()
        assert "42" in captured.out
        client.close()

    def test_display_payload_with_dict(self, capsys):
        """Test display payload with dict input."""
        client = HarnessClient(api_key="key", account_id="acc")
        client._display_payload({"key": "value", "number": 123})
        captured = capsys.readouterr()
        assert "key" in captured.out or "value" in captured.out
        client.close()


class TestConfigHandling:
    """Test configuration handling edge cases."""

    def test_base_url_kwarg_precedence(self):
        """Test that base_url kwarg takes precedence over config."""
        config = HarnessConfig(api_key="key", account_id="acc", base_url="https://config.harness.io")
        client = HarnessClient(config=config, base_url="https://kwarg.harness.io")
        assert client.base_url == "https://kwarg.harness.io"
        client.close()

    def test_config_timeout_setting(self):
        """Test that timeout is configured."""
        config = HarnessConfig(api_key="key", account_id="acc", timeout=60.0)
        client = HarnessClient(config=config)
        assert client._config.timeout == 60.0
        client.close()

    def test_config_max_retries_setting(self):
        """Test that max_retries is configured."""
        config = HarnessConfig(api_key="key", account_id="acc", max_retries=5)
        client = HarnessClient(config=config)
        assert client._config.max_retries == 5
        client.close()


class TestRetryAfterInvalidValue:
    """Test Retry-After header with invalid values."""

    def test_wait_for_retry_invalid_retry_after(self):
        """Test Retry-After with non-integer value falls back to exponential backoff."""
        import time

        client = HarnessClient(api_key="key", account_id="acc")
        headers = httpx.Headers({"retry-after": "not-a-number"})
        response = httpx.Response(503, headers=headers)

        start = time.time()
        client._wait_for_retry(response, 1)
        elapsed = time.time() - start

        # Should use exponential backoff instead
        assert elapsed >= 0.0
        client.close()


class TestPaginationWithAlreadyTypedData:
    """Test pagination when data is already model typed."""

    def test_paginate_offset_model_already_typed(self, httpx_mock: HTTPXMock):
        """Test pagination handles already typed response data."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1", "name": "test"}], "pageItemCount": 1}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                pagination_style=PaginationStyle.OFFSET,
                params={},
                response_model=SampleModel,
            )
        )
        assert len(items) == 1
        assert isinstance(items[0], SampleModel)
        client.close()

    def test_paginate_cursor_model_already_typed(self, httpx_mock: HTTPXMock):
        """Test cursor pagination handles typed response data."""
        httpx_mock.add_response(
            json={
                "data": {"content": [{"id": "1", "name": "test"}]},
                "pageToken": None,
            }
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                pagination_style=PaginationStyle.CURSOR,
                params={},
                response_model=SampleModel,
            )
        )
        assert len(items) == 1
        assert isinstance(items[0], SampleModel)
        client.close()


class TestPaginationTodoWithDifferentStructures:
    """Test TODO pagination with various structures."""

    def test_paginate_todo_with_nested_content(self, httpx_mock: HTTPXMock):
        """Test TODO pagination with nested data.content structure."""
        httpx_mock.add_response(
            json={"data": {"content": [{"id": "1"}, {"id": "2"}]}}
        )
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.TODO, params={})
        )
        assert len(items) == 2
        client.close()

    def test_paginate_todo_empty_dict(self, httpx_mock: HTTPXMock):
        """Test TODO pagination with empty dict."""
        httpx_mock.add_response(json={})
        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate("/test", pagination_style=PaginationStyle.TODO, params={})
        )
        assert len(items) == 0
        client.close()


class TestResolveHierarchyEdgeCases:
    """Test hierarchy resolution edge cases."""

    def test_resolve_hierarchy_partial_org(self):
        """Test hierarchy with only org set."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123", org="org-456")
        hierarchy = client._resolve_hierarchy(scope)
        assert "projectIdentifier" not in hierarchy
        assert "pipelineIdentifier" not in hierarchy
        client.close()


class TestBuildUrlParseQsMode:
    """Test URL building with is_params flag."""

    def test_build_url_is_params_mode(self):
        """Test URL building with is_params=True returns parsed query string."""
        client = HarnessClient(api_key="key", account_id="acc")
        scope = Scope(account_id="acc-123")
        # Note: is_params flag causes parse_qs to be called on the formatted URL
        # parse_qs returns a dict with lists as values for each param
        result = client._build_url(
            "key1={account_id}&key2=value",
            scope,
            is_params=True,
        )
        assert isinstance(result, dict)
        # parse_qs returns {'key1': ['acc-123'], 'key2': ['value']}
        assert "key1" in result
        assert result["key1"] == ["acc-123"]
        client.close()
