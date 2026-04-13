"""
Full integration tests for P2 B1 APIs (Organizations, Projects) with six required scenarios.

Tests verify request/response flow using pytest-httpx mocking for all six
scenarios across both B1 domains (organizations, projects):
1. 2-page auto-pagination with OFFSET style
2. Typed get() with URL and model confirmation
3. create() with x-api-key and x-account-id headers and request body confirmation
4. ScopeNotSetError when scope not set (projects only)
5. 429 retry via tenacity
6. 401 AuthError with ApiError inheritance
"""

import json
from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from harness_python_sdk import HarnessClient
from harness_python_sdk.exceptions import ApiError, AuthError, ScopeNotSetError
from harness_python_sdk.models.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest,
)
from harness_python_sdk.models.projects import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from harness_python_sdk.scope import Scope


@pytest.fixture
def org_scope() -> Scope:
    """Create a test scope with org for organizations."""
    return Scope(account_id="test-account")


@pytest.fixture
def proj_scope() -> Scope:
    """Create a test scope with org for projects."""
    return Scope(account_id="test-account", org="test-org")


@pytest.fixture
def client() -> HarnessClient:
    """Create a HarnessClient with account-level defaults."""
    return HarnessClient(
        api_key="test-key",
        account_id="test-account",
        default_org="test-org",
    )


@pytest.fixture
def scopeless_client() -> HarnessClient:
    """Create a HarnessClient without default scope for scope validation tests."""
    return HarnessClient(api_key="test-key", account_id="test-account")


# ============================================================================
# Scenario 1: 2-page auto-pagination with OFFSET style
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,response_model",
    [
        ("organizations", "/ng/api/organizations", OrganizationResponse),
        ("projects", "/v1/orgs/test-org/projects", ProjectResponse),
    ],
)
def test_list_autopaginates_two_pages(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_path: str,
    response_model: type,
):
    """Scenario 1: List method auto-paginates through two pages via OFFSET style."""
    base_url = f"https://app.harness.io{base_url_path}"

    # Page 1 response with 2 items
    # Both use /ng/api/ or /v1/ endpoints which return data.content wrapped responses
    if domain_name == "projects":
        # Projects include is_favorite and org
        page1_items = [
            {
                "project": {
                    "identifier": f"{domain_name}-1",
                    "name": f"{domain_name.capitalize()} 1",
                    "org": "test-org",
                },
                "isFavorite": False,
            },
            {
                "project": {
                    "identifier": f"{domain_name}-2",
                    "name": f"{domain_name.capitalize()} 2",
                    "org": "test-org",
                },
                "isFavorite": False,
            },
        ]
        page1_response = {
            "data": {
                "content": page1_items,
                "pageIndex": 0,
                "pageSize": 2,
            }
        }
        page2_response = {
            "data": {
                "content": [
                    {
                        "project": {
                            "identifier": f"{domain_name}-2b",
                            "name": f"{domain_name.capitalize()} 2B",
                            "org": "test-org",
                        },
                        "isFavorite": False,
                    },
                ],
                "pageIndex": 1,
                "pageSize": 2,
            }
        }
    else:
        # Organizations use /ng/api/organizations endpoint with data.content wrapper
        # Each item in content wraps the org data: {"organization": {...}, createdAt, lastModifiedAt, harnessManaged}
        page1_items = [
            {
                "organization": {
                    "identifier": f"{domain_name}-1",
                    "name": f"{domain_name.capitalize()} 1",
                },
                "createdAt": 1757514970919,
                "lastModifiedAt": 1757514970920,
                "harnessManaged": False,
            },
            {
                "organization": {
                    "identifier": f"{domain_name}-2",
                    "name": f"{domain_name.capitalize()} 2",
                },
                "createdAt": 1757514970919,
                "lastModifiedAt": 1757514970920,
                "harnessManaged": False,
            },
        ]
        page1_response = {
            "data": {
                "content": page1_items,
                "pageIndex": 0,
                "pageSize": 2,
            }
        }
        page2_response = {
            "data": {
                "content": [
                    {
                        "organization": {
                            "identifier": f"{domain_name}-2b",
                            "name": f"{domain_name.capitalize()} 2B",
                        },
                        "createdAt": 1757514970919,
                        "lastModifiedAt": 1757514970920,
                        "harnessManaged": False,
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
    domain_api = getattr(client, domain_name)
    results = list(domain_api.list(pageSize=2))

    # Assertions
    assert len(results) == 3, f"Expected 3 results (2 on page 1, 1 on page 2), got {len(results)}"
    assert all(isinstance(r, response_model) for r in results), f"Not all results are {response_model}"
    assert len(httpx_mock.get_requests()) == 2, "Expected 2 HTTP requests (2 pages)"


# ============================================================================
# Scenario 2: Typed get() with URL and model confirmation
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param,response_model,payload",
    [
        (
            "organizations",
            "/ng/api/organizations/{id}",
            "org1",
            OrganizationResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "organization": {"identifier": "org1", "name": "Test Organization"},
                    "createdAt": 1757514970919,
                    "lastModifiedAt": 1757514970920,
                    "harnessManaged": False,
                },
            },
        ),
        (
            "projects",
            "/v1/orgs/test-org/projects/{id}",
            "proj1",
            ProjectResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "project": {
                        "identifier": "proj1",
                        "name": "Test Project",
                        "org": "test-org",
                    },
                    "created": 1757514970919,
                    "updated": 1757514970920,
                    "isFavorite": False,
                },
            },
        ),
    ],
)
def test_get_returns_typed_model(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
    response_model: type,
    payload: dict,
):
    """Scenario 2: Get method returns typed response model with correct URL."""
    url = f"https://app.harness.io{base_url_template.format(id=resource_id_param)}"

    # Mock the response
    httpx_mock.add_response(method="GET", url=url, json=payload, status_code=200)

    # Call get()
    domain_api = getattr(client, domain_name)
    result = domain_api.get(resource_id_param)

    # Assertions
    assert isinstance(result, response_model), f"Result is not {response_model}"
    assert result.identifier == resource_id_param
    assert "Test" in result.name

    # Verify URL was called correctly
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert resource_id_param in requests[0].url.path


# ============================================================================
# Scenario 3: create() with x-api-key and x-account-id headers
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,create_request_class,request_kwargs,response_payload",
    [
        (
            "organizations",
            "/ng/api/organizations",
            OrganizationCreateRequest,
            {"identifier": "org1", "name": "Test Organization"},
            {
                "status": "SUCCESS",
                "data": {
                    "organization": {"identifier": "org1", "name": "Test Organization"},
                    "createdAt": 1757514970919,
                    "lastModifiedAt": 1757514970920,
                    "harnessManaged": False,
                },
            },
        ),
        (
            "projects",
            "/v1/orgs/test-org/projects",
            ProjectCreateRequest,
            {"identifier": "proj1", "name": "Test Project"},
            {
                "status": "SUCCESS",
                "data": {
                    "project": {
                        "identifier": "proj1",
                        "name": "Test Project",
                        "org": "test-org",
                    },
                    "created": 1757514970919,
                    "updated": 1757514970920,
                    "isFavorite": False,
                },
            },
        ),
    ],
)
def test_create_sends_headers_and_body(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_path: str,
    create_request_class: type,
    request_kwargs: dict,
    response_payload: dict,
):
    """Scenario 3: Create sends correct x-api-key and x-account-id headers."""
    url = f"https://app.harness.io{base_url_path}"

    # Mock the response
    httpx_mock.add_response(method="POST", url=url, json=response_payload, status_code=201)

    # Create request
    body = create_request_class(**request_kwargs)

    # Call create()
    domain_api = getattr(client, domain_name)
    result = domain_api.create(body)

    # Assertions - check headers
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    req = requests[0]

    assert req.headers.get("x-api-key") == "test-key", "x-api-key header mismatch"
    assert req.headers.get("x-account-id") == "test-account", "x-account-id header mismatch"

    # Assertions - check body
    request_body = json.loads(req.content)
    # For organizations, body should be wrapped: {"organization": {...}}
    if domain_name == "organizations":
        assert "organization" in request_body, "Organizations request should wrap in 'organization' field"
        org_data = request_body["organization"]
        assert org_data["identifier"] == request_kwargs["identifier"]
        assert org_data["name"] == request_kwargs["name"]
    else:
        # Projects also wrap in "project" field
        assert "project" in request_body, "Projects request should wrap in 'project' field"
        proj_data = request_body["project"]
        assert proj_data["identifier"] == request_kwargs["identifier"]
        assert proj_data["name"] == request_kwargs["name"]


# ============================================================================
# Scenario 4: ScopeNotSetError on missing default scope
# ============================================================================


def test_projects_list_raises_scope_not_set_error(
    scopeless_client: HarnessClient,
):
    """Scenario 4: Projects list raises ScopeNotSetError when no org scope provided."""
    with pytest.raises(ScopeNotSetError):
        list(scopeless_client.projects.list())


# ============================================================================
# Scenario 5: 429 retry via tenacity
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param,response_model,payload",
    [
        (
            "organizations",
            "/ng/api/organizations/{id}",
            "org1",
            OrganizationResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "organization": {"identifier": "org1", "name": "Test Organization"},
                    "createdAt": 1757514970919,
                    "lastModifiedAt": 1757514970920,
                    "harnessManaged": False,
                },
            },
        ),
        (
            "projects",
            "/v1/orgs/test-org/projects/{id}",
            "proj1",
            ProjectResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "project": {
                        "identifier": "proj1",
                        "name": "Test Project",
                        "org": "test-org",
                    },
                    "created": 1757514970919,
                    "updated": 1757514970920,
                    "isFavorite": False,
                },
            },
        ),
    ],
)
def test_get_retries_on_429(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
    response_model: type,
    payload: dict,
):
    """Scenario 5: Get retries on 429 (rate limited) response."""
    url = f"https://app.harness.io{base_url_template.format(id=resource_id_param)}"

    # First request returns 429, second returns 200
    httpx_mock.add_response(
        method="GET", url=url, status_code=429, json={"error": "rate limited"}
    )
    httpx_mock.add_response(method="GET", url=url, json=payload, status_code=200)

    # Call get() - should retry and succeed
    domain_api = getattr(client, domain_name)
    result = domain_api.get(resource_id_param)

    # Assertions
    assert isinstance(result, response_model)
    assert result.identifier == resource_id_param
    # Should have made 2 requests (1 failed, 1 succeeded)
    assert len(httpx_mock.get_requests()) == 2


# ============================================================================
# Scenario 6: 401 AuthError with ApiError inheritance
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param",
    [
        (
            "organizations",
            "/ng/api/organizations/{id}",
            "org1",
        ),
        (
            "projects",
            "/v1/orgs/test-org/projects/{id}",
            "proj1",
        ),
    ],
)
def test_get_raises_auth_error_on_401(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
):
    """Scenario 6: Get raises AuthError on 401 response (inherits from ApiError)."""
    url = f"https://app.harness.io{base_url_template.format(id=resource_id_param)}"

    # Mock 401 response
    httpx_mock.add_response(
        method="GET",
        url=url,
        status_code=401,
        json={"error": "unauthorized"},
    )

    # Call get() - should raise AuthError
    domain_api = getattr(client, domain_name)
    with pytest.raises(AuthError) as exc_info:
        domain_api.get(resource_id_param)

    # Verify it's also an ApiError
    assert isinstance(exc_info.value, ApiError)
    assert exc_info.value.status_code == 401
