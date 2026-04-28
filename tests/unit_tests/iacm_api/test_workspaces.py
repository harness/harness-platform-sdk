"""Unit tests for Workspaces IACM API."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.iacm_api.workspaces import (
    WorkspaceCreateRequest,
    WorkspaceResponse,
)
from harness_python_sdk.iacm_api.workspaces import WorkspacesApi
from harness_python_sdk.scope import Scope


class TestWorkspacesApi:
    """Test suite for WorkspacesApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._default_scope = MagicMock(
            account_id="acc123", org="org123", project="proj123"
        )
        client._resolve_scope = MagicMock(
            return_value=Scope(
                account_id="acc123",
                org="org123",
                project="proj123",
            )
        )

        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {
                    "accountId": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                }
            return "/iacm/api/workspaces"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        client._unwrap_response = MagicMock(
            side_effect=lambda key_type=None, raw_data=None, scope=None: raw_data
            or {}
        )
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create WorkspacesApi instance."""
        return WorkspacesApi(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "identifier": "ws1",
            "name": "TestWorkspace",
            "account": "acc123",
            "org": "org123",
            "project": "proj123",
            "provisioner": "terraform",
            "provider_connector": "aws_connector",
            "status": "active",
            "created": 1609459200000,
        }
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("ws1", scope=scope)

        assert result.identifier == "ws1"
        assert result.name == "TestWorkspace"

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        response_data = {
            "identifier": "ws1",
            "name": "TestWorkspace",
            "accountId": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "provisioner": "terraform",
            "providerConnector": "aws_connector",
            "status": "active",
            "createdAt": 1609459200000,
        }
        mock_client._post = MagicMock(return_value=response_data)

        body = WorkspaceCreateRequest(
            identifier="ws1",
            name="TestWorkspace",
            provisioner="terraform",
            provider_connector="aws_connector",
            repository_branch="main",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.create(body, scope=scope)

        assert result.identifier == "ws1"
        assert result.name == "TestWorkspace"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.delete("ws1", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        response_data = [
            {
                "identifier": "ws1",
                "name": "TestWorkspace1",
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "provisioner": "terraform",
                "status": "active",
            }
        ]
        mock_client._paginate = MagicMock(return_value=iter(response_data))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        results = list(api.list(scope=scope))

        assert len(results) == 1
        assert results[0].identifier == "ws1"

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        with pytest.raises(ApiError):
            api.delete("ws1", scope=scope)

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/iacm/api"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key == "none"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "none"

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is False

    def test_update_success(self, api, mock_client):
        """Test successful update operation."""
        response_data = {
            "identifier": "ws1",
            "name": "UpdatedWorkspace",
            "account": "acc123",
            "org": "org123",
            "project": "proj123",
            "provisioner": "terraform",
            "provider_connector": "aws_connector",
            "status": "active",
        }
        mock_client._put = MagicMock(return_value=response_data)

        body = WorkspaceCreateRequest(
            identifier="ws1",
            name="UpdatedWorkspace",
            provisioner="terraform",
            provider_connector="aws_connector",
            repository_branch="main",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.update("ws1", body, scope=scope)

        assert result.name == "UpdatedWorkspace"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = WorkspaceCreateRequest(
            identifier="ws1",
            name="TestWorkspace",
            provisioner="terraform",
            provider_connector="aws_connector",
            repository_branch="main",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_list_empty(self, api, mock_client):
        """Test list with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_create_missing_required_fields(self):
        """Test create request validation."""
        with pytest.raises(ValueError):
            WorkspaceCreateRequest(
                identifier="ws1",
                name="TestWorkspace",
                provisioner="terraform",
                provider_connector="aws_connector",
            )

    def test_wrapped_body(self, api):
        """Test _wrapped_body method."""
        body = WorkspaceCreateRequest(
            identifier="ws1",
            name="TestWorkspace",
            provisioner="terraform",
            provider_connector="aws_connector",
            repository_branch="main",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        api.resolved_scope = scope
        wrapped = api._wrapped_body(body)

        assert wrapped["identifier"] == "ws1"

    def test_unwrapped_response(self, api):
        """Test _unwrapped_response method."""
        response_data = {
            "identifier": "ws1",
            "name": "TestWorkspace",
            "account": "acc123",
            "org": "org123",
            "project": "proj123",
            "provisioner": "terraform",
            "provider_connector": "aws_connector",
            "status": "active",
        }
        result = api._unwrapped_response(response_data)

        assert isinstance(result, WorkspaceResponse)
        assert result.identifier == "ws1"
