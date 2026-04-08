"""
Integration tests for P1 domain APIs.

Tests verify that the API methods work correctly with mocked HTTP responses.
"""

import pytest

from harness_python_sdk import HarnessClient
from harness_python_sdk.exceptions import AuthError, ScopeNotSetError
from harness_python_sdk.models.connectors import ConnectorCreateRequest
from harness_python_sdk.models.infrastructure import InfrastructureCreateRequest
from harness_python_sdk.models.pipelines import PipelineCreateRequest
from harness_python_sdk.models.secrets import SecretCreateRequest
from harness_python_sdk.scope import Scope


@pytest.fixture
def client(httpx_mock):
    """Create a HarnessClient with default scope."""
    return HarnessClient(
        api_key="test-key",
        account_id="test-account",
        default_org="test-org",
        default_project="test-project",
    )


@pytest.fixture
def scope():
    """Create a test scope."""
    return Scope(
        account_id="test-account",
        org="test-org",
        project="test-project",
    )


class TestPipelinesAPI:
    """Tests for Pipelines API."""

    def test_pipelines_api_exists_on_client(self, client):
        """Client has pipelines property."""
        assert hasattr(client, "pipelines")
        assert client.pipelines is not None

    def test_pipelines_get_method_exists(self, client):
        """Pipelines API has get method."""
        assert hasattr(client.pipelines, "get")
        assert callable(client.pipelines.get)

    def test_pipelines_list_method_exists(self, client):
        """Pipelines API has list method."""
        assert hasattr(client.pipelines, "list")
        assert callable(client.pipelines.list)

    def test_pipelines_create_method_exists(self, client):
        """Pipelines API has create method."""
        assert hasattr(client.pipelines, "create")
        assert callable(client.pipelines.create)

    def test_pipelines_update_method_exists(self, client):
        """Pipelines API has update method."""
        assert hasattr(client.pipelines, "update")
        assert callable(client.pipelines.update)

    def test_pipelines_delete_method_exists(self, client):
        """Pipelines API has delete method."""
        assert hasattr(client.pipelines, "delete")
        assert callable(client.pipelines.delete)


class TestConnectorsAPI:
    """Tests for Connectors API."""

    def test_connectors_api_exists_on_client(self, client):
        """Client has connectors property."""
        assert hasattr(client, "connectors")
        assert client.connectors is not None

    def test_connectors_get_method_exists(self, client):
        """Connectors API has get method."""
        assert hasattr(client.connectors, "get")
        assert callable(client.connectors.get)

    def test_connectors_list_method_exists(self, client):
        """Connectors API has list method."""
        assert hasattr(client.connectors, "list")
        assert callable(client.connectors.list)

    def test_connectors_create_method_exists(self, client):
        """Connectors API has create method."""
        assert hasattr(client.connectors, "create")
        assert callable(client.connectors.create)

    def test_connectors_update_method_exists(self, client):
        """Connectors API has update method."""
        assert hasattr(client.connectors, "update")
        assert callable(client.connectors.update)

    def test_connectors_delete_method_exists(self, client):
        """Connectors API has delete method."""
        assert hasattr(client.connectors, "delete")
        assert callable(client.connectors.delete)


class TestSecretsAPI:
    """Tests for Secrets API."""

    def test_secrets_api_exists_on_client(self, client):
        """Client has secrets property."""
        assert hasattr(client, "secrets")
        assert client.secrets is not None

    def test_secrets_get_method_exists(self, client):
        """Secrets API has get method."""
        assert hasattr(client.secrets, "get")
        assert callable(client.secrets.get)

    def test_secrets_list_method_exists(self, client):
        """Secrets API has list method."""
        assert hasattr(client.secrets, "list")
        assert callable(client.secrets.list)

    def test_secrets_create_method_exists(self, client):
        """Secrets API has create method."""
        assert hasattr(client.secrets, "create")
        assert callable(client.secrets.create)

    def test_secrets_update_method_exists(self, client):
        """Secrets API has update method."""
        assert hasattr(client.secrets, "update")
        assert callable(client.secrets.update)

    def test_secrets_delete_method_exists(self, client):
        """Secrets API has delete method."""
        assert hasattr(client.secrets, "delete")
        assert callable(client.secrets.delete)


class TestInfrastructureAPI:
    """Tests for Infrastructure API."""

    def test_infrastructure_api_exists_on_client(self, client):
        """Client has infrastructure property."""
        assert hasattr(client, "infrastructure")
        assert client.infrastructure is not None

    def test_infrastructure_get_method_exists(self, client):
        """Infrastructure API has get method."""
        assert hasattr(client.infrastructure, "get")
        assert callable(client.infrastructure.get)

    def test_infrastructure_list_method_exists(self, client):
        """Infrastructure API has list method."""
        assert hasattr(client.infrastructure, "list")
        assert callable(client.infrastructure.list)

    def test_infrastructure_create_method_exists(self, client):
        """Infrastructure API has create method."""
        assert hasattr(client.infrastructure, "create")
        assert callable(client.infrastructure.create)

    def test_infrastructure_update_method_exists(self, client):
        """Infrastructure API has update method."""
        assert hasattr(client.infrastructure, "update")
        assert callable(client.infrastructure.update)

    def test_infrastructure_delete_method_exists(self, client):
        """Infrastructure API has delete method."""
        assert hasattr(client.infrastructure, "delete")
        assert callable(client.infrastructure.delete)


class TestScopeValidation:
    """Tests for scope validation across all APIs."""

    def test_list_without_scope_raises_scope_not_set_error_pipelines(self):
        """List raises ScopeNotSetError when scope not set (pipelines)."""
        client = HarnessClient(api_key="test-key", account_id="test-account")
        with pytest.raises(ScopeNotSetError):
            list(client.pipelines.list())


class TestAPIAcceptsTypedRequests:
    """Tests that APIs accept typed request models."""

    def test_pipelines_create_accepts_typed_request(self, client, scope, httpx_mock):
        """Pipelines create accepts PipelineCreateRequest."""
        httpx_mock.add_response(
            method="POST",
            url="https://app.harness.io/v1/orgs/test-org/projects/test-project/pipelines",
            json={"identifier": "p1", "name": "P1"},
            status_code=201,
        )

        body = PipelineCreateRequest(
            identifier="p1",
            name="P1",
            pipeline_yaml="yaml",
        )
        # Should not raise
        result = client.pipelines.create(body, scope=scope)
        assert result.identifier == "p1"

    def test_connectors_create_accepts_typed_request(self, client, scope, httpx_mock):
        """Connectors create accepts ConnectorCreateRequest."""
        httpx_mock.add_response(
            method="POST",
            url="https://app.harness.io/ng/api/connectors",
            json={"identifier": "c1", "name": "C1"},
            status_code=201,
        )

        body = ConnectorCreateRequest(
            identifier="c1",
            name="C1",
            spec={},
        )
        result = client.connectors.create(body, scope=scope)
        assert result.identifier == "c1"

    def test_secrets_create_accepts_typed_request(self, client, scope, httpx_mock):
        """Secrets create accepts SecretCreateRequest."""
        httpx_mock.add_response(
            method="POST",
            url="https://app.harness.io/ng/api/v2/secrets",
            json={"identifier": "s1", "name": "S1"},
            status_code=201,
        )

        body = SecretCreateRequest(
            identifier="s1",
            name="S1",
            spec={},
        )
        result = client.secrets.create(body, scope=scope)
        assert result.identifier == "s1"

    def test_infrastructure_create_accepts_typed_request(self, client, scope, httpx_mock):
        """Infrastructure create accepts InfrastructureCreateRequest."""
        httpx_mock.add_response(
            method="POST",
            url="https://app.harness.io/ng/api/infrastructures",
            json={"identifier": "i1", "name": "I1", "type": "Kubernetes"},
            status_code=201,
        )

        body = InfrastructureCreateRequest(
            identifier="i1",
            name="I1",
            type="Kubernetes",
            environment="prod",
        )
        result = client.infrastructure.create(body, scope=scope)
        assert result.identifier == "i1"
