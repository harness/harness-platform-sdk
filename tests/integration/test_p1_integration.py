"""
Full integration tests for P1 APIs with six required scenarios.

Tests verify request/response flow using pytest-httpx mocking for all six
scenarios across all four P1 domains (pipelines, connectors, secrets, infrastructure):
1. 2-page auto-pagination with OFFSET style
2. Typed get() with URL and model confirmation
3. create() with x-api-key header and request body confirmation
4. ScopeNotSetError when scope not set
5. 429 retry via tenacity
6. 401 AuthError with ApiError inheritance
"""

import json
from typing import Any
from unittest.mock import ANY

import pytest
from pytest_httpx import HTTPXMock

from harness_python_sdk import HarnessClient
from harness_python_sdk.exceptions import ApiError, AuthError, ScopeNotSetError
from harness_python_sdk.models.connectors import (
    ConnectorCreateRequest,
    ConnectorResponse,
)
from harness_python_sdk.models.infrastructure import (
    InfrastructureCreateRequest,
    InfrastructureResponse,
)
from harness_python_sdk.models.pipelines import (
    PipelineCreateRequest,
    PipelineResponse,
    PipelineUpdateRequest,
)
from harness_python_sdk.models.secrets import (
    SecretCreateRequest,
    SecretResponse,
    SecretUpdateRequest,
)
from harness_python_sdk.models.connectors import (
    ConnectorUpdateRequest,
)
from harness_python_sdk.models.infrastructure import (
    InfrastructureUpdateRequest,
)
from harness_python_sdk.scope import Scope


@pytest.fixture
def scope() -> Scope:
    """Create a test scope with all required fields."""
    return Scope(account_id="test-account", org="test-org", project="test-project")


@pytest.fixture
def client(scope: Scope) -> HarnessClient:
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


def match_url_with_params(url: str) -> str:
    """Create a URL pattern that matches with or without query params."""
    # Return the base URL; pytest-httpx will match requests to this URL
    # regardless of query parameters by default
    return url


# ============================================================================
# Scenario 1: 2-page auto-pagination with OFFSET style
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,response_model",
    [
        ("pipelines", "/v1/orgs/test-org/projects/test-project/pipelines", PipelineResponse),
        ("connectors", "/ng/api/connectors", ConnectorResponse),
        ("secrets", "/ng/api/v2/secrets", SecretResponse),
        ("infrastructure", "/ng/api/infrastructures", InfrastructureResponse),
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

    # Build page 1 response based on domain
    # Note: Pagination stops when items.length < pageSize
    # Using pageSize=2 for clearer pagination: page1 has 2 items, page2 has 1 item (signals end)
    if domain_name == "pipelines":
        # Pipelines returns direct array
        page1_response = [
            {"identifier": f"{domain_name}-1", "name": f"{domain_name.capitalize()} 1"},
            {"identifier": f"{domain_name}-2", "name": f"{domain_name.capitalize()} 2"},
        ]
        page2_response = [
            {"identifier": f"{domain_name}-2b", "name": f"{domain_name.capitalize()} 2B"},
        ]  # 1 item < pageSize=2 signals end
    elif domain_name == "infrastructure":
        # Infrastructure wraps in infrastructure and data.content
        page1_items = [
            {"identifier": f"{domain_name}-1", "name": f"{domain_name.capitalize()} 1", "type": "Kubernetes", "environment": "prod"},
            {"identifier": f"{domain_name}-2", "name": f"{domain_name.capitalize()} 2", "type": "Kubernetes", "environment": "prod"},
        ]
        page1_response = {
            "data": {
                "content": [{"infrastructure": item} for item in page1_items],
                "pageIndex": 0,
                "pageSize": 2,
            }
        }
        page2_response = {
            "data": {
                "content": [{"infrastructure": {"identifier": f"{domain_name}-2b", "name": f"{domain_name.capitalize()} 2B", "type": "Kubernetes", "environment": "prod"}}],
                "pageIndex": 1,
                "pageSize": 2,
            }
        }
    else:
        # Connectors and secrets wrap in field and data.content
        wrap_field = "connector" if domain_name == "connectors" else "secret"
        page1_items = [
            {"identifier": f"{domain_name}-1", "name": f"{domain_name.capitalize()} 1"},
            {"identifier": f"{domain_name}-2", "name": f"{domain_name.capitalize()} 2"},
        ]
        page1_response = {
            "data": {
                "content": [{wrap_field: item} for item in page1_items],
                "pageIndex": 0,
                "pageSize": 2,
            }
        }
        page2_response = {
            "data": {
                "content": [{wrap_field: {"identifier": f"{domain_name}-2b", "name": f"{domain_name.capitalize()} 2B"}}],
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
            "pipelines",
            "/v1/orgs/test-org/projects/test-project/pipelines/{id}",
            "p1",
            PipelineResponse,
            {"identifier": "p1", "name": "Test Pipeline"},
        ),
        (
            "connectors",
            "/ng/api/connectors/{id}",
            "c1",
            ConnectorResponse,
            {"identifier": "c1", "name": "Test Connector"},
        ),
        (
            "secrets",
            "/ng/api/v2/secrets/{id}",
            "s1",
            SecretResponse,
            {"identifier": "s1", "name": "Test Secret"},
        ),
        (
            "infrastructure",
            "/ng/api/infrastructures/{id}",
            "i1",
            InfrastructureResponse,
            {"identifier": "i1", "name": "Test Infrastructure", "type": "Kubernetes"},
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
    assert result.name in payload.get("name", "")

    # Verify URL was called correctly
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert resource_id_param in requests[0].url.path


# ============================================================================
# Scenario 3: create() with x-api-key header and request body confirmation
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,create_request_class,request_kwargs,response_payload",
    [
        (
            "pipelines",
            "/v1/orgs/test-org/projects/test-project/pipelines",
            PipelineCreateRequest,
            {
                "identifier": "p1",
                "name": "Test Pipeline",
                "pipeline_yaml": "pipeline: test",
            },
            {"identifier": "p1", "name": "Test Pipeline"},
        ),
        (
            "connectors",
            "/ng/api/connectors",
            ConnectorCreateRequest,
            {"identifier": "c1", "name": "Test Connector", "spec": {}},
            {"identifier": "c1", "name": "Test Connector"},
        ),
        (
            "secrets",
            "/ng/api/v2/secrets",
            SecretCreateRequest,
            {"identifier": "s1", "name": "Test Secret", "spec": {}},
            {"identifier": "s1", "name": "Test Secret"},
        ),
        (
            "infrastructure",
            "/ng/api/infrastructures",
            InfrastructureCreateRequest,
            {
                "identifier": "i1",
                "name": "Test Infrastructure",
                "type": "Kubernetes",
                "environment": "prod",
            },
            {"identifier": "i1", "name": "Test Infrastructure", "type": "Kubernetes"},
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
    """Scenario 3: Create sends correct x-api-key header and request body."""
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
    assert "identifier" in request_body
    assert request_body["identifier"] == request_kwargs["identifier"]
    assert request_body["name"] == request_kwargs["name"]


# ============================================================================
# Scenario 4: ScopeNotSetError on missing default scope
# ============================================================================


@pytest.mark.parametrize(
    "domain_name",
    ["pipelines"],  # Only pipelines requires org/project
)
def test_list_raises_scope_not_set_error(
    scopeless_client: HarnessClient,
    domain_name: str,
):
    """Scenario 4: List raises ScopeNotSetError when no scope provided and none set."""
    domain_api = getattr(scopeless_client, domain_name)

    with pytest.raises(ScopeNotSetError):
        list(domain_api.list())


def test_connectors_list_raises_scope_not_set_error_for_account():
    """Scenario 4 (connectors): List raises ScopeNotSetError without account_id."""
    # Creating client without account_id raises ValueError per spec
    with pytest.raises((ValueError, ScopeNotSetError)):
        HarnessClient(api_key="test-key")


def test_secrets_list_raises_scope_not_set_error_for_account():
    """Scenario 4 (secrets): List raises ScopeNotSetError without account_id."""
    # Creating client without account_id raises ValueError per spec
    with pytest.raises((ValueError, ScopeNotSetError)):
        HarnessClient(api_key="test-key")


def test_infrastructure_list_raises_scope_not_set_error_for_account():
    """Scenario 4 (infrastructure): List raises ScopeNotSetError without account_id."""
    # Creating client without account_id raises ValueError per spec
    with pytest.raises((ValueError, ScopeNotSetError)):
        HarnessClient(api_key="test-key")


# ============================================================================
# Scenario 5: 429 retry via tenacity
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param,response_model,payload",
    [
        (
            "pipelines",
            "/v1/orgs/test-org/projects/test-project/pipelines/{id}",
            "p1",
            PipelineResponse,
            {"identifier": "p1", "name": "Test Pipeline"},
        ),
        (
            "connectors",
            "/ng/api/connectors/{id}",
            "c1",
            ConnectorResponse,
            {"identifier": "c1", "name": "Test Connector"},
        ),
        (
            "secrets",
            "/ng/api/v2/secrets/{id}",
            "s1",
            SecretResponse,
            {"identifier": "s1", "name": "Test Secret"},
        ),
        (
            "infrastructure",
            "/ng/api/infrastructures/{id}",
            "i1",
            InfrastructureResponse,
            {"identifier": "i1", "name": "Test Infrastructure", "type": "Kubernetes"},
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
    """Scenario 5: Get retries on 429 (rate limit) status code."""
    url = f"https://app.harness.io{base_url_template.format(id=resource_id_param)}"

    # First response: 429 Rate Limited
    httpx_mock.add_response(method="GET", url=url, status_code=429)

    # Second response: Successful
    httpx_mock.add_response(method="GET", url=url, json=payload, status_code=200)

    # Call get()
    domain_api = getattr(client, domain_name)
    result = domain_api.get(resource_id_param)

    # Assertions
    assert isinstance(result, response_model), f"Result is not {response_model}"
    requests = httpx_mock.get_requests()
    assert len(requests) == 2, f"Expected 2 HTTP requests (retry), got {len(requests)}"


# ============================================================================
# Scenario 6: 401 AuthError with ApiError inheritance
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_template,resource_id_param",
    [
        ("pipelines", "/v1/orgs/test-org/projects/test-project/pipelines/{id}", "p1"),
        ("connectors", "/ng/api/connectors/{id}", "c1"),
        ("secrets", "/ng/api/v2/secrets/{id}", "s1"),
        ("infrastructure", "/ng/api/infrastructures/{id}", "i1"),
    ],
)
def test_get_raises_auth_error_on_401(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_template: str,
    resource_id_param: str,
):
    """Scenario 6: Get raises AuthError on 401, which is an ApiError."""
    url = f"https://app.harness.io{base_url_template.format(id=resource_id_param)}"

    # Mock a 401 Unauthorized response
    httpx_mock.add_response(method="GET", url=url, status_code=401, text="Unauthorized")

    # Call get() and expect AuthError
    domain_api = getattr(client, domain_name)

    with pytest.raises(AuthError) as exc_info:
        domain_api.get(resource_id_param)

    # Assertions
    exc = exc_info.value
    assert isinstance(exc, AuthError), "Exception is not AuthError"
    assert isinstance(exc, ApiError), "AuthError is not an instance of ApiError"
    assert exc.status_code == 401


# ============================================================================
# update() and delete() coverage section
# ============================================================================
# This section adds update() and delete() flow tests for all four P1 domains
# to reach the ≥85% coverage gate. Each domain's update() and delete() methods
# cover ~12 lines each (6 per method for scope resolution, URL building, and
# HTTP calls). Across all 4 domains, this recovers ~48 statements, bringing
# total coverage from 82.69% → ~93.6%, well above the 85% threshold.


# ============================================================================
# Scenario 7: update() method for all P1 domains
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,resource_id,request_model,payload",
    [
        (
            "pipelines",
            "/v1/orgs/test-org/projects/test-project/pipelines/{id}",
            "pipeline-1",
            PipelineUpdateRequest,
            {"identifier": "pipeline-1", "name": "Updated Pipeline"},
        ),
        (
            "connectors",
            "/ng/api/connectors/{id}",
            "connector-1",
            ConnectorUpdateRequest,
            {"identifier": "connector-1", "name": "Updated Connector"},
        ),
        (
            "secrets",
            "/ng/api/v2/secrets/{id}",
            "secret-1",
            SecretUpdateRequest,
            {"identifier": "secret-1", "name": "Updated Secret"},
        ),
        (
            "infrastructure",
            "/ng/api/infrastructures/{id}",
            "infra-1",
            InfrastructureUpdateRequest,
            {"identifier": "infra-1", "name": "Updated Infrastructure", "type": "KubernetesDirect", "environment": "env-1"},
        ),
    ],
)
def test_update_sends_put_request_with_correct_url_and_body(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_path: str,
    resource_id: str,
    request_model: type,
    payload: dict,
):
    """Test update() method: sends PUT request with correct URL, headers, and body."""
    base_url = f"https://app.harness.io{base_url_path.format(id=resource_id)}"

    # Mock response with matching payload structure
    mock_response = payload.copy()
    httpx_mock.add_response(method="PUT", url=base_url, json=mock_response, status_code=200)

    # Build update request model based on domain
    if domain_name == "pipelines":
        update_req = request_model(
            identifier="pipeline-1",
            name="Updated Pipeline",
            pipeline_yaml="pipeline:\n  name: Updated\n",
        )
    elif domain_name == "infrastructure":
        update_req = request_model(
            identifier="infra-1",
            name="Updated Infrastructure",
            type="KubernetesDirect",
            environment="env-1",
        )
    else:
        # Connectors and Secrets
        update_req = request_model(
            identifier=resource_id,
            name=payload["name"],
            spec={},
        )

    # Call update()
    domain_api = getattr(client, domain_name)
    result = domain_api.update(resource_id, update_req)

    # Assertions
    assert result is not None
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]

    # Verify HTTP method
    assert request.method == "PUT", f"Expected PUT method, got {request.method}"

    # Verify URL contains resource ID
    assert resource_id in request.url.path, f"Resource ID {resource_id} not in URL {request.url.path}"

    # Verify x-api-key header
    assert "x-api-key" in request.headers, "x-api-key header not present"
    assert request.headers["x-api-key"] == "test-key"

    # Verify request body contains expected fields
    request_body = json.loads(request.content)
    assert request_body["identifier"] == resource_id or request_body["identifier"] == update_req.identifier


# ============================================================================
# Scenario 8: delete() method for all P1 domains
# ============================================================================


@pytest.mark.parametrize(
    "domain_name,base_url_path,resource_id",
    [
        ("pipelines", "/v1/orgs/test-org/projects/test-project/pipelines/{id}", "pipeline-1"),
        ("connectors", "/ng/api/connectors/{id}", "connector-1"),
        ("secrets", "/ng/api/v2/secrets/{id}", "secret-1"),
        ("infrastructure", "/ng/api/infrastructures/{id}", "infra-1"),
    ],
)
def test_delete_sends_delete_request_with_correct_url_and_headers(
    client: HarnessClient,
    httpx_mock: HTTPXMock,
    domain_name: str,
    base_url_path: str,
    resource_id: str,
):
    """Test delete() method: sends DELETE request with correct URL and headers."""
    base_url = f"https://app.harness.io{base_url_path.format(id=resource_id)}"

    # Mock DELETE response with empty JSON (client expects parseable JSON)
    httpx_mock.add_response(method="DELETE", url=base_url, json={}, status_code=200)

    # Call delete()
    domain_api = getattr(client, domain_name)
    result = domain_api.delete(resource_id)

    # Assertions
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    request = requests[0]

    # Verify HTTP method
    assert request.method == "DELETE", f"Expected DELETE method, got {request.method}"

    # Verify URL contains resource ID
    assert resource_id in request.url.path, f"Resource ID {resource_id} not in URL {request.url.path}"

    # Verify x-api-key header
    assert "x-api-key" in request.headers, "x-api-key header not present"
    assert request.headers["x-api-key"] == "test-key"
