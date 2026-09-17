"""Unit tests for ConnectorsApi."""

from unittest.mock import MagicMock

import pytest

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.exceptions import ApiError
from harness_platform_sdk.models.ng_api.connectors import (
    ConnectorCreateRequest,
    ConnectorResponse,
)
from harness_platform_sdk.ng_api.connectors import ConnectorsApi
from harness_platform_sdk.scope import Scope


class TestConnectorsApi:
    """Test suite for ConnectorsApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(
            return_value=Scope(account_id="acc123", org="org123", project="proj123")
        )

        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {
                    "accountIdentifier": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                }
            return "/ng/api/connectors"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create ConnectorsApi instance."""
        return ConnectorsApi(mock_client)

    @pytest.fixture
    def sample_connector_response(self):
        """Sample connector response."""
        return {
            "identifier": "github_connector",
            "name": "GitHub Connector",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "description": "Test connector",
            "category": "source_repo_provider",
            "type": "Github",
            "spec": {},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_init(self, mock_client):
        """Test ConnectorsApi initialization."""
        api = ConnectorsApi(mock_client)
        assert api._client == mock_client

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/ng/api/connectors"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "connector"

    def test_get_success(self, api, mock_client, sample_connector_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"connector": sample_connector_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_connector_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("github_connector", scope=scope)

        assert result.identifier == "github_connector"
        mock_client._get.assert_called_once()

    def test_get_not_found(self, api, mock_client):
        """Test get operation with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_create_success(self, api, mock_client, sample_connector_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"connector": sample_connector_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_connector_response)

        body = ConnectorCreateRequest(
            identifier="github_connector",
            name="GitHub Connector",
            type="Github",
            spec={},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "github_connector"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = ConnectorCreateRequest(identifier="", name="", type="", spec={})
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_update_success(self, api, mock_client, sample_connector_response):
        """Test successful update operation."""
        updated = sample_connector_response.copy()
        updated["name"] = "Updated GitHub Connector"
        mock_client._put = MagicMock(return_value={"connector": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = ConnectorCreateRequest(
            identifier="github_connector",
            name="Updated GitHub Connector",
            type="Github",
            spec={},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("github_connector", body, scope=scope)

        assert result.name == "Updated GitHub Connector"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("github_connector", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_connector_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=iter([ConnectorResponse(**sample_connector_response)])
        )

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 1
        assert results[0].identifier == "github_connector"

    def test_wrapped_body_wraps_connector(self, api):
        """Test _wrapped_body wraps request correctly."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = ConnectorCreateRequest(identifier="conn1", name="Test", type="Github", spec={})
        wrapped = api._wrapped_body(body)

        assert "connector" in wrapped

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("conn1", scope=scope)

        assert result == {}
