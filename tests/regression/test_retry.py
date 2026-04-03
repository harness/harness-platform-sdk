"""Regression tests for retry behavior."""

import pytest
from pytest_httpx import HTTPXMock

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.config import HarnessConfig
from harness_python_sdk.exceptions import ApiError


class TestRetryBehavior:
    """Test retry logic for transient failures."""

    def test_retry_on_429(self, httpx_mock: HTTPXMock):
        """Test that 429 responses are retried."""
        # First request fails with 429, second succeeds
        httpx_mock.add_response(status_code=429)
        httpx_mock.add_response(status_code=429)
        httpx_mock.add_response(json={"success": True})

        client = HarnessClient(
            api_key="key",
            account_id="acc",
        )
        result = client._get("/test")
        assert result["success"] is True
        client.close()

    def test_retry_on_503(self, httpx_mock: HTTPXMock):
        """Test that 503 responses are retried."""
        httpx_mock.add_response(status_code=503)
        httpx_mock.add_response(status_code=503)
        httpx_mock.add_response(json={"success": True})

        client = HarnessClient(api_key="key", account_id="acc")
        result = client._get("/test")
        assert result["success"] is True
        client.close()

    def test_no_retry_on_4xx_except_429(self, httpx_mock: HTTPXMock):
        """Test that 4xx responses (except 429) are not retried."""
        httpx_mock.add_response(status_code=400, text="Bad Request")

        client = HarnessClient(api_key="key", account_id="acc")
        with pytest.raises(ApiError):
            client._get("/test")
        client.close()

    def test_no_retry_on_5xx_except_503(self, httpx_mock: HTTPXMock):
        """Test that 5xx responses (except 503) are not retried."""
        httpx_mock.add_response(status_code=500, text="Internal Server Error")

        client = HarnessClient(api_key="key", account_id="acc")
        with pytest.raises(ApiError):
            client._get("/test")
        client.close()

    def test_retry_disabled_via_config(self, httpx_mock: HTTPXMock):
        """Test that retry can be disabled via config."""
        httpx_mock.add_response(status_code=429)

        config = HarnessConfig(
            api_key="key",
            account_id="acc",
            retry_enabled=False,
        )
        client = HarnessClient(config=config)
        with pytest.raises(ApiError):
            client._get("/test")
        client.close()

    def test_custom_retry_status_codes(self, httpx_mock: HTTPXMock):
        """Test that custom retry_status_codes are respected."""
        # 500 should be retried if in retry_status_codes
        httpx_mock.add_response(status_code=500)
        httpx_mock.add_response(status_code=500)
        httpx_mock.add_response(json={"success": True})

        config = HarnessConfig(
            api_key="key",
            account_id="acc",
            retry_status_codes=[429, 500, 503],
        )
        client = HarnessClient(config=config)
        result = client._get("/test")
        assert result["success"] is True
        client.close()

    def test_max_retries_respected(self, httpx_mock: HTTPXMock):
        """Test that max_retries limit is respected."""
        # max_retries=2 means 3 total attempts (initial + 2 retries)
        for _ in range(3):
            httpx_mock.add_response(status_code=429)

        config = HarnessConfig(
            api_key="key",
            account_id="acc",
            max_retries=2,  # Only 2 retries, so 3 total attempts
        )
        client = HarnessClient(config=config)
        with pytest.raises(ApiError):
            client._get("/test")
        client.close()
