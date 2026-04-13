"""
Full integration tests for P2 B3 APIs (Roles, ResourceGroups, RoleAssignments) with six required scenarios.

Tests verify request/response flow using pytest-httpx mocking for all six
scenarios across all three B3 RBAC domains (all org-scoped):
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
from harness_python_sdk.models.resource_groups import (
    ResourceGroupCreateRequest,
    ResourceGroupResponse,
)
from harness_python_sdk.models.role_assignments import (
    RoleAssignmentCreateRequest,
    RoleAssignmentResponse,
)
from harness_python_sdk.models.roles import (
    RoleCreateRequest,
    RoleResponse,
)
from harness_python_sdk.scope import Scope


@pytest.fixture
def client() -> HarnessClient:
    """Create a HarnessClient with default org scope."""
    return HarnessClient(
        api_key="test-key",
        account_id="test-account",
        default_org="test-org",
    )


@pytest.fixture
def scopeless_client() -> HarnessClient:
    """Create a HarnessClient without default scope."""
    return HarnessClient(api_key="test-key", account_id="test-account")


# ============================================================================
# Scenario 1: 2-page auto-pagination with OFFSET style
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,response_model",
    [
        ("roles", "/v1/orgs/test-org/roles", RoleResponse),
        ("resource_groups", "/v1/orgs/test-org/resource-groups", ResourceGroupResponse),
        (
            "role_assignments",
            "/v1/orgs/test-org/role-assignments",
            RoleAssignmentResponse,
        ),
    ],
)
def test_rbac_list_autopaginates_two_pages(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_path: str,
    response_model: type,
):
    """Scenario 1: RBAC list methods auto-paginate through two pages via OFFSET style."""
    base_url = f"https://app.harness.io{base_url_path}"

    # Page 1 response with 2 items
    if domain_name == "roles":
        page1_items = [
            {
                "identifier": "role-1",
                "name": "Role 1",
                "allowedScopeLevels": ["ORG", "PROJECT"],
            },
            {
                "identifier": "role-2",
                "name": "Role 2",
                "allowedScopeLevels": ["ORG"],
            },
        ]
        page2_items = [
            {
                "identifier": "role-2b",
                "name": "Role 2B",
                "allowedScopeLevels": ["ACCOUNT", "ORG"],
            },
        ]
    elif domain_name == "resource_groups":
        page1_items = [
            {"identifier": "rg-1", "name": "Resource Group 1"},
            {"identifier": "rg-2", "name": "Resource Group 2"},
        ]
        page2_items = [
            {"identifier": "rg-2b", "name": "Resource Group 2B"},
        ]
    else:  # role_assignments
        page1_items = [
            {
                "identifier": "ra-1",
                "roleIdentifier": "admin",
                "scope": {"scopeType": "ORG"},
                "principal": {"type": "USER", "identifier": "user1"},
            },
            {
                "identifier": "ra-2",
                "roleIdentifier": "viewer",
                "scope": {"scopeType": "ORG"},
                "principal": {"type": "USER", "identifier": "user2"},
            },
        ]
        page2_items = [
            {
                "identifier": "ra-2b",
                "roleIdentifier": "editor",
                "scope": {"scopeType": "ORG"},
                "principal": {"type": "USER", "identifier": "user3"},
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
            "content": page2_items,
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
    assert all(isinstance(r, response_model) for r in results)
    assert len(httpx_mock.get_requests()) == 2, "Expected 2 HTTP requests (2 pages)"


# ============================================================================
# Scenario 2: Typed get() with URL and model confirmation
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param,response_model,payload",
    [
        (
            "roles",
            "/v1/orgs/test-org/roles/{id}",
            "role1",
            RoleResponse,
            {
                "identifier": "role1",
                "name": "Test Role",
                "allowedScopeLevels": ["ORG"],
                "created": 1234567890,
                "updated": 1234567890,
            },
        ),
        (
            "resource_groups",
            "/v1/orgs/test-org/resource-groups/{id}",
            "rg1",
            ResourceGroupResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "resourceGroup": {
                        "identifier": "rg1",
                        "name": "Test Resource Group",
                    },
                    "createdAt": 1234567890,
                    "lastModifiedAt": 1234567890,
                    "harnessManaged": False,
                },
            },
        ),
        (
            "role_assignments",
            "/v1/orgs/test-org/role-assignments/{id}",
            "ra1",
            RoleAssignmentResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "role-assignment": {
                        "identifier": "ra1",
                        "roleIdentifier": "admin",
                        "scope": {"scopeType": "ORG"},
                        "principal": {"type": "USER", "identifier": "user1"},
                    },
                    "created": 1234567890,
                    "updated": 1234567890,
                    "harness_managed": False,
                },
            },
        ),
    ],
)
def test_rbac_get_returns_typed_model(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
    response_model: type,
    payload: dict,
):
    """Scenario 2: RBAC get methods return typed response model with correct URL."""
    url = f"https://app.harness.io{base_url_template.format(id=resource_id_param)}"

    httpx_mock.add_response(method="GET", url=url, json=payload, status_code=200)

    # Call get()
    domain_api = getattr(client, domain_name)
    result = domain_api.get(resource_id_param)

    # Assertions
    assert isinstance(result, response_model)
    assert result.identifier == resource_id_param

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
            "roles",
            "/v1/orgs/test-org/roles",
            RoleCreateRequest,
            {
                "identifier": "role1",
                "name": "Test Role",
                "allowed_scope_levels": ["ORG"],
            },
            {
                "identifier": "role1",
                "name": "Test Role",
                "allowedScopeLevels": ["ORG"],
                "created": 1234567890,
                "updated": 1234567890,
            },
        ),
        (
            "resource_groups",
            "/v1/orgs/test-org/resource-groups",
            ResourceGroupCreateRequest,
            {"identifier": "rg1", "name": "Test Resource Group"},
            {
                "status": "SUCCESS",
                "data": {
                    "resourceGroup": {
                        "identifier": "rg1",
                        "name": "Test Resource Group",
                    },
                    "createdAt": 1234567890,
                    "lastModifiedAt": 1234567890,
                    "harnessManaged": False,
                },
            },
        ),
        (
            "role_assignments",
            "/v1/orgs/test-org/role-assignments",
            RoleAssignmentCreateRequest,
            {
                "role_identifier": "admin",
                "scope": {"scopeType": "ORG"},
                "principal": {"type": "USER", "identifier": "user1"},
            },
            {
                "status": "SUCCESS",
                "data": {
                    "role-assignment": {
                        "identifier": "ra1",
                        "roleIdentifier": "admin",
                        "scope": {"scopeType": "ORG"},
                        "principal": {"type": "USER", "identifier": "user1"},
                    },
                    "created": 1234567890,
                    "updated": 1234567890,
                    "harness_managed": False,
                },
            },
        ),
    ],
)
def test_rbac_create_sends_headers_and_body(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_path: str,
    create_request_class: type,
    request_kwargs: dict,
    response_payload: dict,
):
    """Scenario 3: RBAC create methods send correct x-api-key and x-account-id headers."""
    url = f"https://app.harness.io{base_url_path}"

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
    if domain_name == "roles":
        # roles are flat
        assert "identifier" in request_body
        assert request_body["identifier"] == "role1"
        assert "allowedScopeLevels" in request_body
    elif domain_name == "resource_groups":
        # resource_groups are wrapped in "resourceGroup"
        assert "resourceGroup" in request_body
        assert request_body["resourceGroup"]["identifier"] == "rg1"
    else:  # role_assignments
        # role_assignments are wrapped in "role-assignment"
        assert "role-assignment" in request_body
        assert request_body["role-assignment"]["roleIdentifier"] == "admin"


# ============================================================================
# Scenario 4: ScopeNotSetError on missing default scope
# ============================================================================


@pytest.mark.parametrize(
    "domain_name",
    ["roles", "resource_groups", "role_assignments"],
)
def test_rbac_list_raises_scope_not_set_error(
    scopeless_client: HarnessClient,
    domain_name: str,
):
    """Scenario 4: RBAC list raises ScopeNotSetError when no org scope provided."""
    domain_api = getattr(scopeless_client, domain_name)
    with pytest.raises(ScopeNotSetError):
        list(domain_api.list())


# ============================================================================
# Scenario 5: 429 retry via tenacity
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param,response_model,payload",
    [
        (
            "roles",
            "/v1/orgs/test-org/roles/{id}",
            "role1",
            RoleResponse,
            {
                "identifier": "role1",
                "name": "Test Role",
                "allowedScopeLevels": ["ORG"],
                "created": 1234567890,
                "updated": 1234567890,
            },
        ),
        (
            "resource_groups",
            "/v1/orgs/test-org/resource-groups/{id}",
            "rg1",
            ResourceGroupResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "resourceGroup": {
                        "identifier": "rg1",
                        "name": "Test Resource Group",
                    },
                    "createdAt": 1234567890,
                    "lastModifiedAt": 1234567890,
                    "harnessManaged": False,
                },
            },
        ),
        (
            "role_assignments",
            "/v1/orgs/test-org/role-assignments/{id}",
            "ra1",
            RoleAssignmentResponse,
            {
                "status": "SUCCESS",
                "data": {
                    "role-assignment": {
                        "identifier": "ra1",
                        "roleIdentifier": "admin",
                        "scope": {"scopeType": "ORG"},
                        "principal": {"type": "USER", "identifier": "user1"},
                    },
                    "created": 1234567890,
                    "updated": 1234567890,
                    "harness_managed": False,
                },
            },
        ),
    ],
)
def test_rbac_get_retries_on_429(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
    response_model: type,
    payload: dict,
):
    """Scenario 5: RBAC get methods retry on 429 (rate limited) response."""
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
            "roles",
            "/v1/orgs/test-org/roles/{id}",
            "role1",
        ),
        (
            "resource_groups",
            "/v1/orgs/test-org/resource-groups/{id}",
            "rg1",
        ),
        (
            "role_assignments",
            "/v1/orgs/test-org/role-assignments/{id}",
            "ra1",
        ),
    ],
)
def test_rbac_get_raises_auth_error_on_401(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
):
    """Scenario 6: RBAC get raises AuthError on 401 response (inherits from ApiError)."""
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
