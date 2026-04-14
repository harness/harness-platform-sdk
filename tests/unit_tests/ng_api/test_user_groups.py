"""Unit tests for UserGroupsApi."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.ng_api.user_groups import (
    UserGroupCreateRequest,
    UserGroupResponse,
)
from harness_python_sdk.ng_api.user_groups import UserGroupsApi
from harness_python_sdk.scope import Scope


class TestUserGroupsApi:
    """Test suite for UserGroupsApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(
            return_value=Scope(account_id="acc123", org="org123")
        )
        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {"accountIdentifier": "acc123", "orgIdentifier": "org123"}
            return "/ng/api/user-groups"
        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create UserGroupsApi instance."""
        return UserGroupsApi(mock_client)

    @pytest.fixture
    def sample_group_response(self):
        """Sample user group response."""
        return {
            "identifier": "engineers",
            "name": "Engineering Team",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "description": "Engineering group",
            "users": ["user1", "user2"],
            "tags": {"team": "engineering"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_get_success(self, api, mock_client, sample_group_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"userGroup": sample_group_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_group_response)

        scope = Scope(account_id="acc123", org="org123")
        result = api.get("engineers", scope=scope)

        assert result.identifier == "engineers"

    def test_create_success(self, api, mock_client, sample_group_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"userGroup": sample_group_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_group_response)

        body = UserGroupCreateRequest(
            identifier="engineers",
            name="Engineering Team",
        )
        scope = Scope(account_id="acc123", org="org123")
        result = api.create(body, scope=scope)

        assert result.identifier == "engineers"

    def test_update_success(self, api, mock_client, sample_group_response):
        """Test successful update operation."""
        updated = sample_group_response.copy()
        updated["name"] = "Senior Engineers"
        mock_client._put = MagicMock(return_value={"userGroup": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = UserGroupCreateRequest(
            identifier="engineers",
            name="Senior Engineers",
        )
        scope = Scope(account_id="acc123", org="org123")
        result = api.update("engineers", body, scope=scope)

        assert result.name == "Senior Engineers"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123")
        result = api.delete("engineers", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_group_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=iter([UserGroupResponse(**sample_group_response)])
        )

        scope = Scope(account_id="acc123", org="org123")
        results = list(api.list(scope=scope))

        assert len(results) == 1

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = UserGroupCreateRequest(identifier="engineers", name="Team")
        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.delete("engineers", scope=scope)

    def test_list_empty(self, api, mock_client):
        """Test list with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123")
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_wrapped_body_structure(self, api):
        """Test _wrapped_body structure."""
        api._resolved_scope = Scope(account_id="acc123", org="org123")
        body = UserGroupCreateRequest(identifier="group1", name="Test")
        wrapped = api._wrapped_body(body)

        assert "userGroup" not in wrapped

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = UserGroupCreateRequest(identifier="engineers", name="Updated")
        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)
