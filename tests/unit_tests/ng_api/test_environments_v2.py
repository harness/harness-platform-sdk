"""Unit tests for EnvironmentsV2Api."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.ng_api.environments_v2 import (
    EnvironmentV2CreateRequest,
    EnvironmentV2Response,
)
from harness_python_sdk.ng_api.environments_v2 import EnvironmentsV2Api
from harness_python_sdk.scope import Scope


class TestEnvironmentsV2Api:
    """Test suite for EnvironmentsV2Api."""

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
            return "/ng/api/environment-v2"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create EnvironmentsV2Api instance."""
        return EnvironmentsV2Api(mock_client)

    @pytest.fixture
    def sample_env_response(self):
        """Sample environment response."""
        return {
            "identifier": "prod_env",
            "name": "Production Environment",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "description": "Production environment",
            "variables": {},
            "type": "PreProduction",
            "tags": {"tier": "prod"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_init(self, mock_client):
        """Test EnvironmentsV2Api initialization."""
        api = EnvironmentsV2Api(mock_client)
        assert api._client == mock_client

    def test_get_success(self, api, mock_client, sample_env_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"environment": sample_env_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_env_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("prod_env", scope=scope)

        assert result.identifier == "prod_env"

    def test_create_success(self, api, mock_client, sample_env_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"environment": sample_env_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_env_response)

        body = EnvironmentV2CreateRequest(
            identifier="prod_env",
            name="Production Environment",
            type="Production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "prod_env"

    def test_update_success(self, api, mock_client, sample_env_response):
        """Test successful update operation."""
        updated = sample_env_response.copy()
        updated["name"] = "Updated Production"
        mock_client._put = MagicMock(return_value={"environment": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = EnvironmentV2CreateRequest(
            identifier="prod_env",
            name="Updated Production",
            type="Production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("prod_env", body, scope=scope)

        assert result.name == "Updated Production"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("prod_env", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_env_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=iter([EnvironmentV2Response(**sample_env_response)])
        )

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 1

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = EnvironmentV2CreateRequest(identifier="", name="", type="")
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("prod_env", scope=scope)

    def test_wrapped_body_structure(self, api):
        """Test _wrapped_body structure."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = EnvironmentV2CreateRequest(identifier="env1", name="Test", type="Production")
        wrapped = api._wrapped_body(body)

        assert "identifier" in wrapped
        assert "name" in wrapped
        assert "type" in wrapped
        assert "accountIdentifier" in wrapped
        assert "orgIdentifier" in wrapped
        assert "projectIdentifier" in wrapped

    def test_list_empty(self, api, mock_client):
        """Test list with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 0
