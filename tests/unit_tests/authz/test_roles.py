"""Unit tests for RolesApi."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.authz.roles import RolesApi
from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.authz.roles import (
    RoleCreateRequest,
    RoleResponse,
)
from harness_python_sdk.scope import Scope


class TestRolesApi:
    """Test suite for RolesApi."""

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
            return "/authz/api/roles"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create RolesApi instance."""
        return RolesApi(mock_client)

    @pytest.fixture
    def sample_role_response(self):
        """Sample role response."""
        return {
            "identifier": "admin_role",
            "name": "Admin Role",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "allowedScopeLevels": ["account", "org", "project"],
            "description": "Administrator role",
            "permissions": ["admin_all"],
            "disabled": False,
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_get_success(self, api, mock_client, sample_role_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"role": sample_role_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_role_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("admin_role", scope=scope)

        assert result.identifier == "admin_role"

    def test_create_success(self, api, mock_client, sample_role_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"role": sample_role_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_role_response)

        body = RoleCreateRequest(
            identifier="admin_role",
            name="Admin Role",
            allowed_scope_levels=["account", "org", "project"],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "admin_role"

    def test_update_success(self, api, mock_client, sample_role_response):
        """Test successful update operation."""
        updated = sample_role_response.copy()
        updated["name"] = "Super Admin"
        mock_client._put = MagicMock(return_value={"role": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = RoleCreateRequest(
            identifier="admin_role",
            name="Super Admin",
            allowed_scope_levels=["account", "org", "project"],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("admin_role", body, scope=scope)

        assert result.name == "Super Admin"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("admin_role", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_role_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(return_value=iter([RoleResponse(**sample_role_response)]))

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

        body = RoleCreateRequest(
            identifier="admin_role",
            name="Admin",
            allowed_scope_levels=["account"],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("admin_role", scope=scope)

    def test_list_multiple(self, api, mock_client, sample_role_response):
        """Test list with multiple roles."""
        role2 = sample_role_response.copy()
        role2["identifier"] = "viewer_role"

        roles = [
            RoleResponse(**sample_role_response),
            RoleResponse(**role2),
        ]
        mock_client._paginate = MagicMock(return_value=iter(roles))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 2

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = RoleCreateRequest(
            identifier="admin_role",
            name="Updated",
            allowed_scope_levels=["account"],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)

    def test_should_wrap_false(self, api):
        """Test that roles don't wrap body."""
        assert api.should_wrap is False

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/authz/api/roles"
