"""Unit tests for SecretsApi."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.ng_api.secrets import (
    SecretCreateRequest,
    SecretResponse,
)
from harness_python_sdk.ng_api.secrets import SecretsApi
from harness_python_sdk.scope import Scope


class TestSecretsApi:
    """Test suite for SecretsApi."""

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
            return "/ng/api/secrets"
        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create SecretsApi instance."""
        return SecretsApi(mock_client)

    @pytest.fixture
    def sample_secret_response(self):
        """Sample secret response."""
        return {
            "identifier": "db_password",
            "name": "Database Password",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "description": "DB password secret",
            "type": "SecretText",
            "spec": {
                "secretManagerIdentifier": "harnessSecretManager",
                "valueType": "Inline",
                "value": "changeme",
            },
            "tags": {"app": "backend"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_get_success(self, api, mock_client, sample_secret_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"secret": sample_secret_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_secret_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("db_password", scope=scope)

        assert result.identifier == "db_password"

    def test_create_success(self, api, mock_client, sample_secret_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"secret": sample_secret_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_secret_response)

        body = SecretCreateRequest(
            identifier="db_password",
            name="Database Password",
            type="SecretText",
            spec={
                "secretManagerIdentifier": "harnessSecretManager",
                "valueType": "Inline",
                "value": "changeme",
            },
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "db_password"

    def test_update_success(self, api, mock_client, sample_secret_response):
        """Test successful update operation."""
        updated = sample_secret_response.copy()
        updated["name"] = "Updated DB Password"
        mock_client._put = MagicMock(return_value={"secret": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = SecretCreateRequest(
            identifier="db_password",
            name="Updated DB Password",
            type="SecretText",
            spec={
                "secretManagerIdentifier": "harnessSecretManager",
                "valueType": "Inline",
                "value": "changeme",
            },
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("db_password", body, scope=scope)

        assert result.name == "Updated DB Password"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("db_password", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_secret_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=iter([SecretResponse(**sample_secret_response)])
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

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = SecretCreateRequest(identifier="db_password", name="Test", type="SecretText", spec={})
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("db_password", scope=scope)

    def test_list_empty(self, api, mock_client):
        """Test list with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_wrapped_body_structure(self, api):
        """Test _wrapped_body structure."""
        api._resolved_scope = Scope(
            account_id="acc123", org="org123", project="proj123"
        )
        body = SecretCreateRequest(identifier="secret1", name="Test", type="SecretText", spec={})
        wrapped = api._wrapped_body(body)

        assert "secret" in wrapped

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = SecretCreateRequest(identifier="db_password", name="Updated", type="SecretText", spec={})
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)
