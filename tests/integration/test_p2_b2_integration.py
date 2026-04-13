"""
Full integration tests for P2 B2 API (Services) with six required scenarios.

Tests verify request/response flow using pytest-httpx mocking for all six
scenarios for the services domain:
1. 2-page auto-pagination with OFFSET style
2. Typed get() with URL and model confirmation
3. create() with x-api-key and x-account-id headers and request body confirmation
4. ScopeNotSetError when scope not set
5. 429 retry via tenacity
6. 401 AuthError with ApiError inheritance
"""

import json

import pytest
from pytest_httpx import HTTPXMock

from harness_python_sdk import HarnessClient
from harness_python_sdk.exceptions import ApiError, AuthError, ScopeNotSetError
from harness_python_sdk.models.services import (
    ServiceCreateRequest,
    ServiceResponse,
    ServiceUpdateRequest,
)
from harness_python_sdk.scope import Scope


@pytest.fixture
def client() -> HarnessClient:
    """Create a HarnessClient with default scope."""
    return HarnessClient(
        api_key="test-key",
        account_id="test-account",
        default_org="test-org",
        default_project="test-project",
    )


@pytest.fixture
def scopeless_client() -> HarnessClient:
    """Create a HarnessClient without default scope for scope validation tests."""
    return HarnessClient(api_key="test-key", account_id="test-account")


# ============================================================================
# Scenario 1: 2-page auto-pagination with OFFSET style
# ============================================================================


def test_services_list_autopaginates_two_pages(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
):
    """Scenario 1: Services list auto-paginates through two pages via OFFSET style."""
    base_url = "https://app.harness.io/v1/orgs/test-org/projects/test-project/services"

    # Page 1 response with 2 items
    page1_items = [
        {
            "identifier": "service-1",
            "name": "Service 1",
            "org": "test-org",
            "project": "test-project",
        },
        {
            "identifier": "service-2",
            "name": "Service 2",
            "org": "test-org",
            "project": "test-project",
        },
    ]
    page1_response = {
        "data": {
            "content": page1_items,
            "pageIndex": 0,
            "pageSize": 2,
        }
    }

    # Page 2 response with 1 item (signals end of pagination)
    page2_response = {
        "data": {
            "content": [
                {
                    "identifier": "service-2b",
                    "name": "Service 2B",
                    "org": "test-org",
                    "project": "test-project",
                },
            ],
            "pageIndex": 1,
            "pageSize": 2,
        }
    }

    # Register responses with match_params for query parameters
    httpx_mock.add_response(
        method="GET",
        url=base_url,
        json=page1_response,
        match_params={"pageIndex": "0", "pageSize": "2"},
    )
    httpx_mock.add_response(
        method="GET",
        url=base_url,
        json=page2_response,
        match_params={"pageIndex": "1", "pageSize": "2"},
    )

    # Call list() with pageSize=2 to force 2-page pagination
    results = list(client.services.list(pageSize=2))

    # Assertions
    assert len(results) == 3, f"Expected 3 results (2 on page 1, 1 on page 2), got {len(results)}"
    assert all(isinstance(r, ServiceResponse) for r in results)
    assert len(httpx_mock.get_requests()) == 2, "Expected 2 HTTP requests (2 pages)"


# ============================================================================
# Scenario 2: Typed get() with URL and model confirmation
# ============================================================================


def test_services_get_returns_typed_model(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
):
    """Scenario 2: Get method returns typed response model with correct URL."""
    url = "https://app.harness.io/v1/orgs/test-org/projects/test-project/services/svc1"
    payload = {
        "status": "SUCCESS",
        "data": {
            "service": {
                "identifier": "svc1",
                "name": "Test Service",
                "org": "test-org",
                "project": "test-project",
            },
            "created": 1234567890,
            "updated": 1234567890,
        },
    }

    httpx_mock.add_response(method="GET", url=url, json=payload, status_code=200)

    # Call get()
    result = client.services.get("svc1")

    # Assertions
    assert isinstance(result, ServiceResponse)
    assert result.identifier == "svc1"
    assert result.name == "Test Service"

    # Verify URL was called correctly
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert "svc1" in requests[0].url.path


# ============================================================================
# Scenario 3: create() with x-api-key and x-account-id headers
# ============================================================================


def test_services_create_sends_headers_and_body(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
):
    """Scenario 3: Create sends correct x-api-key and x-account-id headers."""
    url = "https://app.harness.io/v1/orgs/test-org/projects/test-project/services"
    response_payload = {
        "status": "SUCCESS",
        "data": {
            "service": {
                "identifier": "svc1",
                "name": "Test Service",
                "org": "test-org",
                "project": "test-project",
            },
            "created": 1234567890,
            "updated": 1234567890,
        },
    }

    httpx_mock.add_response(method="POST", url=url, json=response_payload, status_code=201)

    # Create request
    body = ServiceCreateRequest(
        identifier="svc1",
        name="Test Service",
    )

    # Call create()
    result = client.services.create(body)

    # Assertions - check headers
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    req = requests[0]

    assert req.headers.get("x-api-key") == "test-key", "x-api-key header mismatch"
    assert req.headers.get("x-account-id") == "test-account", "x-account-id header mismatch"

    # Assertions - check body (should be wrapped in {"service": {...}})
    request_body = json.loads(req.content)
    assert "service" in request_body, "Request body should be wrapped in 'service' key"
    assert request_body["service"]["identifier"] == "svc1"
    assert request_body["service"]["name"] == "Test Service"


# ============================================================================
# Scenario 4: ScopeNotSetError on missing default scope
# ============================================================================


def test_services_list_raises_scope_not_set_error(
    scopeless_client: HarnessClient,
):
    """Scenario 4: Services list raises ScopeNotSetError when scope not provided."""
    with pytest.raises(ScopeNotSetError):
        list(scopeless_client.services.list())


# ============================================================================
# Scenario 5: 429 retry via tenacity
# ============================================================================


def test_services_get_retries_on_429(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
):
    """Scenario 5: Get retries on 429 (rate limited) response."""
    url = "https://app.harness.io/v1/orgs/test-org/projects/test-project/services/svc1"
    payload = {
        "status": "SUCCESS",
        "data": {
            "service": {
                "identifier": "svc1",
                "name": "Test Service",
                "org": "test-org",
                "project": "test-project",
            },
            "created": 1234567890,
            "updated": 1234567890,
        },
    }

    # First request returns 429, second returns 200
    httpx_mock.add_response(
        method="GET", url=url, status_code=429, json={"error": "rate limited"}
    )
    httpx_mock.add_response(method="GET", url=url, json=payload, status_code=200)

    # Call get() - should retry and succeed
    result = client.services.get("svc1")

    # Assertions
    assert isinstance(result, ServiceResponse)
    assert result.identifier == "svc1"
    # Should have made 2 requests (1 failed, 1 succeeded)
    assert len(httpx_mock.get_requests()) == 2


# ============================================================================
# Scenario 6: 401 AuthError with ApiError inheritance
# ============================================================================


def test_services_get_raises_auth_error_on_401(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
):
    """Scenario 6: Get raises AuthError on 401 response (inherits from ApiError)."""
    url = "https://app.harness.io/v1/orgs/test-org/projects/test-project/services/svc1"

    # Mock 401 response
    httpx_mock.add_response(
        method="GET",
        url=url,
        status_code=401,
        json={"error": "unauthorized"},
    )

    # Call get() - should raise AuthError
    with pytest.raises(AuthError) as exc_info:
        client.services.get("svc1")

    # Verify it's also an ApiError
    assert isinstance(exc_info.value, ApiError)
    assert exc_info.value.status_code == 401
