"""Unit tests for EntityApi."""

from unittest.mock import MagicMock, patch

import pytest

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.exceptions import ApiError
from harness_platform_sdk.idp_api.entities import EntityApi
from harness_platform_sdk.models.idp_api.entities import (
    EntityCreateRequest,
    EntityResourceCreateRequest,
    EntityResponse,
)
from harness_platform_sdk.pagination import PaginationStyle
from harness_platform_sdk.scope import Scope


class TestEntityApi:
    """Test suite for EntityApi."""

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
            return "/v1/entities"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        client._resolve_idp_hierarchy = MagicMock(return_value="org123/proj123")
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create EntityApi instance with mock client."""
        return EntityApi(mock_client)

    @pytest.fixture
    def sample_entity_response(self):
        """Sample entity response."""
        return {
            "identifier": "entity123",
            "name": "Test Entity",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "description": "Test entity",
            "tags": ["prod", "critical"],
            "createdAt": 1234567890000,
            "updatedAt": 1234567890000,
        }

    def test_init(self, mock_client):
        """Test EntityApi initialization."""
        api = EntityApi(mock_client)
        assert api._client == mock_client

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/v1/entities"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key is None

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key is None

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is False

    def test_get_success(self, api, mock_client, sample_entity_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value=sample_entity_response)
        mock_client._unwrap_response = MagicMock(return_value=sample_entity_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("entity123", "resource", scope=scope)

        assert result.identifier == "entity123"
        assert result.name == "Test Entity"
        mock_client._get.assert_called_once()

    def test_get_not_found(self, api, mock_client):
        """Test get operation with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("nonexistent", "resource", scope=scope)

    def test_get_forbidden(self, api, mock_client):
        """Test get operation with 403 error."""
        mock_client._get = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("entity123", "resource", scope=scope)

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("entity123", "resource", scope=scope)

        assert result == {}

    def test_create_success(self, api, mock_client, sample_entity_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value=sample_entity_response)
        mock_client._unwrap_response = MagicMock(return_value=sample_entity_response)

        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            description="Test entity",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "entity123"
        assert result.name == "Test Entity"
        mock_client._post.assert_called_once()

    def test_create_with_missing_scope(self, api, mock_client):
        """Test create without scope raises error."""
        mock_client._resolve_scope = MagicMock(side_effect=ValueError("Scope required"))

        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        with pytest.raises(ValueError):
            api.create(body, scope=None)

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict (409) error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            description="Test entity",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error (400)."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = EntityResourceCreateRequest(
            identifier="",
            name="",
            description="",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_update_success(self, api, mock_client, sample_entity_response):
        """Test successful update operation."""
        updated_response = sample_entity_response.copy()
        updated_response["name"] = "Updated Entity"
        mock_client._put = MagicMock(return_value=updated_response)
        mock_client._unwrap_response = MagicMock(return_value=updated_response)

        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Updated Entity",
            description="Updated",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("entity123", "resource", body, scope=scope)

        assert result.name == "Updated Entity"
        mock_client._put.assert_called_once()

    def test_update_not_found(self, api, mock_client):
        """Test update operation with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Updated",
            description="Updated description",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("nonexistent", "resource", body, scope=scope)

    def test_update_permission_denied(self, api, mock_client):
        """Test update operation with 403 error."""
        mock_client._put = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Updated",
            description="Updated description",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("entity123", "resource", body, scope=scope)

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("entity123", "resource", scope=scope)

        assert result is not None
        mock_client._delete.assert_called_once()

    def test_delete_not_found(self, api, mock_client):
        """Test delete operation with 404 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("nonexistent", "resource", scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete operation with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("entity123", "resource", scope=scope)

    def test_list_single_page(self, api, mock_client, sample_entity_response):
        """Test list operation with single page."""
        mock_client._paginate = MagicMock(
            return_value=iter([EntityResponse(**sample_entity_response)])
        )

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 1
        assert results[0].identifier == "entity123"
        mock_client._paginate.assert_called_once()

    def test_list_multiple_pages(self, api, mock_client, sample_entity_response):
        """Test list operation with multiple pages."""
        entity2 = sample_entity_response.copy()
        entity2["identifier"] = "entity456"
        entity2["name"] = "Entity 2"

        entities = [
            EntityResponse(**sample_entity_response),
            EntityResponse(**entity2),
        ]
        mock_client._paginate = MagicMock(return_value=iter(entities))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 2
        assert results[0].identifier == "entity123"
        assert results[1].identifier == "entity456"

    def test_list_empty(self, api, mock_client):
        """Test list operation with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_list_uses_pagination_style_offset(self, api, mock_client):
        """Test list operation uses OFFSET pagination style."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        list(api.list(scope=scope))

        call_kwargs = mock_client._paginate.call_args[1]
        assert call_kwargs["pagination_style"] == PaginationStyle.OFFSET

    def test_resolved_scope_property(self, api, mock_client):
        """Test resolved_scope property setter."""
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        api.resolved_scope = scope

        assert api.resolved_scope.account_id == "acc123"
        mock_client._resolve_scope.assert_called()

    def test_default_params_property(self, api, mock_client):
        """Test default_params property."""
        mock_client._build_url = MagicMock(
            return_value="accountIdentifier=acc123&orgIdentifier=org123&projectIdentifier=proj123"
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        api.resolved_scope = scope

        params = api.default_params
        assert params is not None

    def test_wrapped_body_injects_scope_identifiers(self, api, mock_client):
        """Test _wrapped_body injects scope identifiers."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            description="Test description",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        wrapped = api._wrapped_body(body)

        # The method returns YAML, so check it contains the identifiers
        assert "acc123" in str(wrapped)
        assert "org123" in str(wrapped)
        assert "proj123" in str(wrapped)

    def test_wrapped_body_sets_api_version(self, api, mock_client):
        """Test _wrapped_body sets API version."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            description="Test description",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        wrapped = api._wrapped_body(body)

        # The method returns YAML, check it contains apiVersion
        assert "harness.io/v1" in str(wrapped)

    def test_wrapped_body_sets_metadata(self, api, mock_client):
        """Test _wrapped_body sets metadata from description."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            description="Test description",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        wrapped = api._wrapped_body(body)

        # The method returns YAML, check it contains metadata
        assert "metadata" in str(wrapped)

    def test_wrapped_body_sets_spec(self, api, mock_client):
        """Test _wrapped_body sets spec with lifecycle."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = EntityResourceCreateRequest(
            identifier="entity123",
            name="Test Entity",
            description="Test description",
            type="resource",
            owner="team123",
            lifecycle="production",
        )
        wrapped = api._wrapped_body(body)

        # The method returns YAML, check it contains spec and lifecycle
        assert "spec" in str(wrapped)
        assert "lifecycle: production" in str(wrapped) or "lifecycle: ' production'" in str(wrapped)

    def test_unwrapped_response(self, api, mock_client, sample_entity_response):
        """Test _unwrapped_response returns EntityResponse."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api._unwrapped_response(sample_entity_response)

        assert isinstance(result, EntityResponse)
        assert result.identifier == "entity123"
