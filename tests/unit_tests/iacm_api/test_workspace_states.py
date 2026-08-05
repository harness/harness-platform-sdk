"""Unit tests for Workspace States IACM API."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.iacm_api.workspace_states import WorkspaceStatesApi
from harness_python_sdk.models.iacm_api.workspace_states import (
    WorkspaceStateCreateRequest,
    WorkspaceStateResponse,
)
from harness_python_sdk.scope import Scope


class TestWorkspaceStatesApi:
    """Test suite for WorkspaceStatesApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._default_scope = MagicMock(account_id="acc123", org="org123", project="proj123")
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
                    "accountIdentifier": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                }
            return "/iacm/api/orgs/org123/projects/proj123/workspaces/ws1/terraform-backend"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        client._unwrap_response = MagicMock(
            side_effect=lambda key_type=None, raw_data=None, scope=None: raw_data or {}
        )
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create WorkspaceStatesApi instance."""
        return WorkspaceStatesApi(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "terraform_version": "1.0.0",
            "serial": 1,
            "version": 4,
            "resources": [{"type": "aws_instance", "name": "example"}],
            "outputs": {"instance_id": {"value": "i-123456"}},
        }
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("ws1", scope=scope)

        assert result.terraform_version == "1.0.0"
        assert result.serial == 1

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        response_data = {
            "terraform_version": "1.0.0",
            "serial": 1,
            "version": 4,
            "resources": [{"type": "aws_instance", "name": "example"}],
        }
        mock_client._post = MagicMock(return_value=response_data)

        body = WorkspaceStateCreateRequest(
            terraform_version="1.0.0",
            serial=1,
            version=4,
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.create("ws1", body, scope=scope)

        assert result.terraform_version == "1.0.0"
        assert result.serial == 1

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

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/iacm/api"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key is None

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key is None

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is False

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = WorkspaceStateCreateRequest(
            terraform_version="1.0.0",
            serial=1,
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        with pytest.raises(ApiError):
            api.create("ws1", body, scope=scope)

    def test_wrapped_body(self, api):
        """Test _wrapped_body method."""
        body = WorkspaceStateCreateRequest(
            terraform_version="1.0.0",
            serial=1,
            version=4,
        )
        wrapped = api._wrapped_body(body)

        assert wrapped == body.model_dump(exclude_none=True)

    def test_unwrapped_response(self, api):
        """Test _unwrapped_response method."""
        response_data = {
            "terraform_version": "1.0.0",
            "serial": 1,
            "version": 4,
        }
        result = api._unwrapped_response("ws1", response_data)

        assert isinstance(result, WorkspaceStateResponse)
        assert result.terraform_version == "1.0.0"

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("ws1", scope=scope)

        assert result == {}
