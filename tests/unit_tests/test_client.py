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
        with pytest.raises(ApiError):
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
