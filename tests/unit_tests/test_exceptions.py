"""Unit tests for exception hierarchy."""

import pytest

from harness_python_sdk.exceptions import (
    ApiError,
    AuthError,
    HarnessSdkError,
    ScopeNotSetError,
)


class TestExceptionHierarchy:
    """Test exception hierarchy and relationships."""

    def test_harness_sdk_error_is_exception(self):
        """Test that HarnessSdkError is an Exception."""
        assert issubclass(HarnessSdkError, Exception)

    def test_scope_not_set_error_inheritance(self):
        """Test that ScopeNotSetError inherits from HarnessSdkError."""
        assert issubclass(ScopeNotSetError, HarnessSdkError)

    def test_api_error_inheritance(self):
        """Test that ApiError inherits from HarnessSdkError."""
        assert issubclass(ApiError, HarnessSdkError)

    def test_auth_error_inheritance(self):
        """Test that AuthError inherits from ApiError."""
        assert issubclass(AuthError, ApiError)

    def test_scope_not_set_error_can_be_raised(self):
        """Test that ScopeNotSetError can be raised and caught."""
        with pytest.raises(ScopeNotSetError):
            raise ScopeNotSetError("org not set")

    def test_scope_not_set_error_message(self):
        """Test ScopeNotSetError message."""
        error = ScopeNotSetError("test message")
        assert str(error) == "test message"


class TestApiError:
    """Test ApiError functionality."""

    def test_api_error_creation(self):
        """Test creating an ApiError."""
        error = ApiError(500, "Internal Server Error", {"content-type": "application/json"})
        assert error.status_code == 500
        assert error.body == "Internal Server Error"
        assert error.headers == {"content-type": "application/json"}

    def test_api_error_str_does_not_expose_body(self):
        """Test that ApiError.__str__ doesn't expose sensitive body content."""
        error = ApiError(500, "sensitive data here", {})
        error_str = str(error)
        assert "sensitive data here" not in error_str
        assert "API error" in error_str
        assert "status_code=500" in error_str

    def test_api_error_args_do_not_expose_body(self):
        """Test that ApiError.args doesn't expose sensitive content."""
        error = ApiError(400, '{"error": "secret"}', {})
        # args should be set from __init__
        assert error.status_code == 400
        # Message should not contain the body
        assert "secret" not in str(error)

    def test_api_error_headers_preserved(self):
        """Test that headers are preserved in ApiError."""
        headers = {"retry-after": "60", "x-request-id": "req-123"}
        error = ApiError(429, "Too Many Requests", headers)
        assert error.headers == headers
        assert error.headers["retry-after"] == "60"


class TestAuthError:
    """Test AuthError functionality."""

    def test_auth_error_creation(self):
        """Test creating an AuthError (401)."""
        error = AuthError(401, "Unauthorized", {"www-authenticate": "Bearer"})
        assert error.status_code == 401
        assert error.body == "Unauthorized"
        assert error.headers == {"www-authenticate": "Bearer"}

    def test_auth_error_403(self):
        """Test creating an AuthError (403)."""
        error = AuthError(403, "Forbidden", {})
        assert error.status_code == 403
        assert error.body == "Forbidden"

    def test_auth_error_is_api_error(self):
        """Test that AuthError is an instance of ApiError."""
        error = AuthError(401, "body", {})
        assert isinstance(error, ApiError)

    def test_auth_error_is_harness_sdk_error(self):
        """Test that AuthError is an instance of HarnessSdkError."""
        error = AuthError(401, "body", {})
        assert isinstance(error, HarnessSdkError)

    def test_auth_error_can_be_caught_as_api_error(self):
        """Test that AuthError can be caught as ApiError."""
        with pytest.raises(ApiError):
            raise AuthError(401, "body", {})

    def test_auth_error_can_be_caught_as_harness_sdk_error(self):
        """Test that AuthError can be caught as HarnessSdkError."""
        with pytest.raises(HarnessSdkError):
            raise AuthError(401, "body", {})


class TestExceptionCatching:
    """Test exception catching patterns."""

    def test_scope_error_not_caught_as_api_error(self):
        """Test that ScopeNotSetError is not caught as ApiError."""
        with pytest.raises(ScopeNotSetError):
            try:
                raise ScopeNotSetError("test")
            except ApiError:
                pytest.fail("ScopeNotSetError caught as ApiError")

    def test_all_exceptions_inherit_from_harness_sdk_error(self):
        """Test that all SDK exceptions inherit from HarnessSdkError."""
        errors = [
            ScopeNotSetError("scope"),
            ApiError(500, "body", {}),
            AuthError(401, "body", {}),
        ]
        for error in errors:
            assert isinstance(error, HarnessSdkError)
