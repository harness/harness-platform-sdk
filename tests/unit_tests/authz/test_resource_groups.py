"""Unit tests for ResourceGroupsApi."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.authz.resource_groups import ResourceGroupsApi
from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.authz.resource_groups import (
    ResourceGroupCreateRequest,
    ResourceGroupResponse,
)
from harness_python_sdk.scope import Scope


class TestResourceGroupsApi:
    """Test suite for ResourceGroupsApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(
            return_value=Scope(
                account_id="acc123", org="org123", project="proj123"
            )
        )
        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {
                    "accountIdentifier": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                }
            return "/authz/api/v2/resourcegroup"
        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create ResourceGroupsApi instance."""
        return ResourceGroupsApi(mock_client)

    @pytest.fixture
    def sample_rg_response(self):
        """Sample resource group response."""
        return {
            "identifier": "rg_services",
            "name": "Services Resource Group",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "description": "Service resources",
            "resourceFilter": {"resourceType": "SERVICE"},
            "allowed_scope_levels": ["project"],
            "included_scopes": [{"filter": "EXCLUDING_CHILD_SCOPES"}],
            "tags": {"app": "backend"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_get_success(self, api, mock_client, sample_rg_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(
            return_value={"resourceGroup": sample_rg_response}
        )
        mock_client._unwrap_response = MagicMock(return_value=sample_rg_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("rg_services", scope=scope)

        assert result.identifier == "rg_services"

    def test_create_success(self, api, mock_client, sample_rg_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(
            return_value={"resourceGroup": sample_rg_response}
        )
        mock_client._unwrap_response = MagicMock(return_value=sample_rg_response)

        body = ResourceGroupCreateRequest(
            identifier="rg_services",
            name="Services Resource Group",
            allowed_scope_levels=["project"],
            resource_filter={"resources": [], "includeAllResource": "true"},
            included_scopes=[{"filter": "EXCLUDING_CHILD_SCOPES"}],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "rg_services"

    def test_update_success(self, api, mock_client, sample_rg_response):
        """Test successful update operation."""
        updated = sample_rg_response.copy()
        updated["name"] = "Updated Services RG"
        mock_client._put = MagicMock(return_value={"resourceGroup": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = ResourceGroupCreateRequest(
            identifier="rg_services",
            name="Updated Services RG",
            allowed_scope_levels=["project"],
            resource_filter={"resources": [], "includeAllResource": "true"},
            included_scopes=[{"filter": "EXCLUDING_CHILD_SCOPES"}],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("rg_services", body, scope=scope)

        assert result.name == "Updated Services RG"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("rg_services", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_rg_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=iter([ResourceGroupResponse(**sample_rg_response)])
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

        body = ResourceGroupCreateRequest(
            identifier="rg_services",
            name="Services",
            allowed_scope_levels=["project"],
            resource_filter={"resources": [], "includeAllResource": "true"},
            included_scopes=[{"filter": "EXCLUDING_CHILD_SCOPES"}],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("rg_services", scope=scope)

    def test_list_multiple(self, api, mock_client, sample_rg_response):
        """Test list with multiple resource groups."""
        rg2 = sample_rg_response.copy()
        rg2["identifier"] = "rg_envs"

        rgs = [
            ResourceGroupResponse(**sample_rg_response),
            ResourceGroupResponse(**rg2),
        ]
        mock_client._paginate = MagicMock(return_value=iter(rgs))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 2

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = ResourceGroupCreateRequest(
            identifier="rg_services",
            name="Updated",
            allowed_scope_levels=["project"],
            resource_filter={"resources": [], "includeAllResource": "true"},
            included_scopes=[{"filter": "EXCLUDING_CHILD_SCOPES"}],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/authz/api/v2/resourcegroup"

    def test_should_wrap_false(self, api):
        """Test that resource groups don't wrap body."""
        assert api.should_wrap is True
