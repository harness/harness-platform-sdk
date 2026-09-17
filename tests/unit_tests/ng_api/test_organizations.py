"""Unit tests for OrganizationsApi."""

from unittest.mock import MagicMock, patch

import pytest

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.exceptions import ApiError
from harness_platform_sdk.models.ng_api.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
)
from harness_platform_sdk.ng_api.organizations import OrganizationsApi
from harness_platform_sdk.scope import Scope


class TestOrganizationsApi:
    """Test suite for OrganizationsApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(return_value=Scope(account_id="acc123"))

        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {"accountIdentifier": "acc123"}
            return "/ng/api/organizations"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create OrganizationsApi instance with mock client."""
        return OrganizationsApi(mock_client)

    @pytest.fixture
    def sample_org_response(self):
        """Sample organization response."""
        return {
            "identifier": "org123",
            "name": "Test Org",
            "accountIdentifier": "acc123",
            "description": "Test organization",
            "tags": {"env": "test"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
            "harnessManaged": False,
        }

    def test_init(self, mock_client):
        """Test OrganizationsApi initialization."""
        api = OrganizationsApi(mock_client)
        assert api._client == mock_client

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/ng/api/organizations"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "organization"

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is True

    def test_get_success(self, api, mock_client, sample_org_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"organization": sample_org_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_org_response)

        scope = Scope(account_id="acc123")
        result = api.get("org123", scope=scope)

        assert result.identifier == "org123"
        assert result.name == "Test Org"
        mock_client._get.assert_called_once()
        mock_client._unwrap_response.assert_called_once()

    def test_get_not_found(self, api, mock_client):
        """Test get operation with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_get_forbidden(self, api, mock_client):
        """Test get operation with 403 error."""
        mock_client._get = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.get("org123", scope=scope)

    def test_create_success(self, api, mock_client, sample_org_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"organization": sample_org_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_org_response)

        body = OrganizationCreateRequest(
            identifier="org123",
            name="Test Org",
            description="Test organization",
            tags={"env": "test"},
        )
        scope = Scope(account_id="acc123")
        result = api.create(body, scope=scope)

        assert result.identifier == "org123"
        assert result.name == "Test Org"
        mock_client._post.assert_called_once()

    def test_create_with_missing_scope(self, api, mock_client):
        """Test create without scope raises error."""
        mock_client._resolve_scope = MagicMock(side_effect=ValueError("Scope required"))

        body = OrganizationCreateRequest(identifier="org123", name="Test Org")
        with pytest.raises(ValueError):
            api.create(body, scope=None)

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict (409) error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = OrganizationCreateRequest(identifier="org123", name="Test Org")
        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error (400)."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = OrganizationCreateRequest(identifier="", name="")
        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_update_success(self, api, mock_client, sample_org_response):
        """Test successful update operation."""
        updated_response = sample_org_response.copy()
        updated_response["name"] = "Updated Org"
        mock_client._put = MagicMock(return_value={"organization": updated_response})
        mock_client._unwrap_response = MagicMock(return_value=updated_response)

        body = OrganizationCreateRequest(
            identifier="org123",
            name="Updated Org",
            description="Updated",
        )
        scope = Scope(account_id="acc123")
        result = api.update("org123", body, scope=scope)

        assert result.name == "Updated Org"
        mock_client._put.assert_called_once()

    def test_update_not_found(self, api, mock_client):
        """Test update operation with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = OrganizationCreateRequest(identifier="org123", name="Updated")
        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)

    def test_update_permission_denied(self, api, mock_client):
        """Test update operation with 403 error."""
        mock_client._put = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        body = OrganizationCreateRequest(identifier="org123", name="Updated")
        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.update("org123", body, scope=scope)

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123")
        result = api.delete("org123", scope=scope)

        assert result is not None
        mock_client._delete.assert_called_once()

    def test_delete_not_found(self, api, mock_client):
        """Test delete operation with 404 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.delete("nonexistent", scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete operation with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123")
        with pytest.raises(ApiError):
            api.delete("org123", scope=scope)

    def test_list_single_page(self, api, mock_client, sample_org_response):
        """Test list operation with single page."""
        mock_client._paginate = MagicMock(
            return_value=iter([OrganizationResponse(**sample_org_response)])
        )

        scope = Scope(account_id="acc123")
        results = list(api.list(scope=scope))

        assert len(results) == 1
        assert results[0].identifier == "org123"
        mock_client._paginate.assert_called_once()

    def test_list_multiple_pages(self, api, mock_client, sample_org_response):
        """Test list operation with multiple pages."""
        org2 = sample_org_response.copy()
        org2["identifier"] = "org456"
        org2["name"] = "Org 2"

        orgs = [
            OrganizationResponse(**sample_org_response),
            OrganizationResponse(**org2),
        ]
        mock_client._paginate = MagicMock(return_value=iter(orgs))

        scope = Scope(account_id="acc123")
        results = list(api.list(scope=scope))

        assert len(results) == 2
        assert results[0].identifier == "org123"
        assert results[1].identifier == "org456"

    def test_list_empty(self, api, mock_client):
        """Test list operation with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123")
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_list_with_search_term(self, api, mock_client, sample_org_response):
        """Test list operation with search term."""
        mock_client._paginate = MagicMock(
            return_value=iter([OrganizationResponse(**sample_org_response)])
        )

        scope = Scope(account_id="acc123")
        results = list(api.list(scope=scope, searchTerm="Test"))

        assert len(results) == 1
        mock_client._paginate.assert_called_once()

    def test_wrapped_body_wraps_organization(self, api, mock_client):
        """Test _wrapped_body wraps request in organization key."""
        api._resolved_scope = Scope(account_id="acc123")
        body = OrganizationCreateRequest(
            identifier="org123",
            name="Test Org",
            description="Test",
        )
        wrapped = api._wrapped_body(body)

        assert "organization" in wrapped
        assert wrapped["organization"]["identifier"] == "org123"

    def test_wrapped_body_injects_account_id(self, api, mock_client):
        """Test _wrapped_body injects account identifier."""
        api._resolved_scope = Scope(account_id="acc123")
        body = OrganizationCreateRequest(identifier="org123", name="Test Org")
        wrapped = api._wrapped_body(body)

        assert wrapped["organization"]["accountIdentifier"] == "acc123"

    def test_resolved_scope_property(self, api, mock_client):
        """Test resolved_scope property setter."""
        scope = Scope(account_id="acc123")
        api.resolved_scope = scope

        assert api.resolved_scope.account_id == "acc123"
        mock_client._resolve_scope.assert_called()

    def test_default_params_property(self, api, mock_client):
        """Test default_params property."""
        mock_client._build_url = MagicMock(return_value="accountIdentifier=acc123")
        scope = Scope(account_id="acc123")
        api.resolved_scope = scope

        params = api.default_params
        assert params is not None

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(account_id="acc123")
        result = api.get("org123", scope=scope)

        assert result == {}
