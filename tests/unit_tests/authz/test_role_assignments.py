"""Unit tests for RoleAssignmentsApi."""

from unittest.mock import MagicMock

import pytest

from harness_platform_sdk.authz.role_assignments import RoleAssignmentsApi
from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.exceptions import ApiError
from harness_platform_sdk.models.authz.role_assignments import (
    RoleAssignmentCreateRequest,
    RoleAssignmentResponse,
)
from harness_platform_sdk.scope import Scope


class TestRoleAssignmentsApi:
    """Test suite for RoleAssignmentsApi."""

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
            return "/authz/api/roleassignments"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create RoleAssignmentsApi instance."""
        return RoleAssignmentsApi(mock_client)

    @pytest.fixture
    def sample_assignment_response(self):
        """Sample role assignment response."""
        return {
            "identifier": "assign_123",
            "role_identifier": "admin_role",
            "resource_group_identifier": "_project_resources",
            "role_reference": {"identifier": "simple_test", "scopeLevel": "project"},
            "principal": {"type": "USER", "identifier": "user123"},
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "disabled": False,
            "createdAt": 1234567890000,
        }

    def test_get_success(self, api, mock_client, sample_assignment_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"roleAssignment": sample_assignment_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_assignment_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("assign_123", scope=scope)

        assert result.identifier == "assign_123"

    def test_create_success(self, api, mock_client, sample_assignment_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"roleAssignment": sample_assignment_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_assignment_response)

        body = RoleAssignmentCreateRequest(
            role_identifier="_project_admin",
            resource_group_identifier="_all_project_level_resources",
            principal={"identifier": "_project_all_users", "type": "USER_GROUP"},
            role_reference={"identifier": "simple_test", "scopeLevel": "project"},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "assign_123"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("assign_123", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_assignment_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=iter([RoleAssignmentResponse(**sample_assignment_response)])
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

        body = RoleAssignmentCreateRequest(
            role_identifier="",
            resource_group_identifier="",
            principal={"identifier": "", "type": "USER_GROUP"},
            role_reference={"identifier": "", "scopeLevel": ""},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("assign_123", scope=scope)

    def test_list_multiple(self, api, mock_client, sample_assignment_response):
        """Test list with multiple assignments."""
        assign2 = sample_assignment_response.copy()
        assign2["identifier"] = "assign_456"

        assignments = [
            RoleAssignmentResponse(**sample_assignment_response),
            RoleAssignmentResponse(**assign2),
        ]
        mock_client._paginate = MagicMock(return_value=iter(assignments))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 2

    def test_list_empty(self, api, mock_client):
        """Test list with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/authz/api/roleassignments"

    def test_should_wrap_false(self, api):
        """Test that role assignments don't wrap body."""
        assert api.should_wrap is False

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "roleAssignment"

    def test_update_success(self, api, mock_client, sample_assignment_response):
        """Test successful update operation."""
        updated_response = sample_assignment_response.copy()
        updated_response["disabled"] = True
        mock_client._put = MagicMock(return_value={"roleAssignment": updated_response})
        mock_client._unwrap_response = MagicMock(return_value=updated_response)

        body = RoleAssignmentCreateRequest(
            role_identifier="_project_admin",
            resource_group_identifier="_all_project_level_resources",
            principal={"identifier": "_project_all_users", "type": "USER_GROUP"},
            role_reference={"identifier": "simple_test", "scopeLevel": "project"},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("assign_123", body, scope=scope)

        assert result.identifier == "assign_123"
        mock_client._put.assert_called_once()

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = RoleAssignmentCreateRequest(
            role_identifier="_project_admin",
            resource_group_identifier="_all_project_level_resources",
            principal={"identifier": "_project_all_users", "type": "USER_GROUP"},
            role_reference={"identifier": "simple_test", "scopeLevel": "project"},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)

    def test_resolved_scope_property(self, api, mock_client):
        """Test resolved_scope property setter."""
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        api.resolved_scope = scope

        assert api.resolved_scope.account_id == "acc123"
        assert api.resolved_scope.org == "org123"
        assert api.resolved_scope.project == "proj123"
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

    def test_wrapped_body_returns_body_when_not_wrapped(self, api):
        """Test _wrapped_body returns body unchanged when should_wrap is False."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = RoleAssignmentCreateRequest(
            role_identifier="_project_admin",
            resource_group_identifier="_all_project_level_resources",
            principal={"identifier": "_project_all_users", "type": "USER_GROUP"},
            role_reference={"identifier": "simple_test", "scopeLevel": "project"},
        )
        wrapped = api._wrapped_body(body)

        assert wrapped == body

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("assign_123", scope=scope)

        assert result == {}

    def test_get_forbidden(self, api, mock_client):
        """Test get with 403 error."""
        mock_client._get = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("assign_123", scope=scope)

    def test_create_forbidden(self, api, mock_client):
        """Test create with 403 error."""
        mock_client._post = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        body = RoleAssignmentCreateRequest(
            role_identifier="_project_admin",
            resource_group_identifier="_all_project_level_resources",
            principal={"identifier": "_project_all_users", "type": "USER_GROUP"},
            role_reference={"identifier": "simple_test", "scopeLevel": "project"},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_not_found(self, api, mock_client):
        """Test delete with 404 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("nonexistent", scope=scope)

    def test_list_with_params(self, api, mock_client, sample_assignment_response):
        """Test list operation with additional parameters."""
        mock_client._paginate = MagicMock(
            return_value=iter([RoleAssignmentResponse(**sample_assignment_response)])
        )

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope, searchTerm="admin"))

        assert len(results) == 1
        mock_client._paginate.assert_called_once()
