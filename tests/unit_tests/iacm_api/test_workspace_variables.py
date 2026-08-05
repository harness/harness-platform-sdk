"""Unit tests for Workspace Variables IACM API."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.iacm_api.workspace_variables import WorkspaceVariablesApi
from harness_python_sdk.models.iacm_api.workspace_variables import (
    WorkspaceValueType,
    WorkspaceVariableCreateRequest,
    WorkspaceVariableKind,
    WorkspaceVariableResponse,
)
from harness_python_sdk.scope import Scope


class TestWorkspaceVariablesApi:
    """Test suite for WorkspaceVariablesApi."""

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
            return "/iacm/api/orgs/org123/projects/proj123/workspaces/ws1/variables"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        client._unwrap_response = MagicMock(
            side_effect=lambda key_type=None, raw_data=None, scope=None: raw_data or {}
        )
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create WorkspaceVariablesApi instance."""
        return WorkspaceVariablesApi(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "account": "acc123",
            "org": "org123",
            "project": "proj123",
            "workspace": "ws1",
            "key": "VAR1",
            "kind": "env",
            "value": "test_value",
            "value_type": "string",
            "created": 1609459200000,
        }
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("VAR1", "ws1", WorkspaceVariableKind.env, scope=scope)

        assert result.identifier == "VAR1"
        assert result.value == "test_value"

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={})

        body = WorkspaceVariableCreateRequest(
            workspace_identifier="ws1",
            identifier="VAR1",
            kind=WorkspaceVariableKind.tf,
            value="test_value",
            value_type=WorkspaceValueType.string,
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.create(body, scope=scope)

        assert result.identifier == "VAR1"

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        response_data = [
            {
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "workspace": "ws1",
                "key": "VAR1",
                "kind": "env",
                "value": "value1",
                "value_type": "string",
            }
        ]
        mock_client._paginate = MagicMock(return_value=iter(response_data))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        results = list(api.list("ws1", scope=scope))

        assert len(results) == 1
        assert results[0].identifier == "VAR1"

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        with pytest.raises(ApiError):
            api.get("nonexistent", "ws1", WorkspaceVariableKind.env, scope=scope)

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

    def test_update_success(self, api, mock_client):
        """Test successful update operation."""
        mock_client._put = MagicMock(return_value={})

        body = WorkspaceVariableCreateRequest(
            workspace_identifier="ws1",
            identifier="VAR1",
            kind=WorkspaceVariableKind.env,
            value="updated_value",
            value_type=WorkspaceValueType.string,
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.update("VAR1", body, scope=scope)

        assert result.value == "updated_value"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = WorkspaceVariableCreateRequest(
            workspace_identifier="ws1",
            identifier="VAR1",
            kind=WorkspaceVariableKind.tf,
            value="test_value",
            value_type=WorkspaceValueType.string,
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
        results = list(api.list("ws1", scope=scope))

        assert len(results) == 0

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.delete("VAR1", "ws1", WorkspaceVariableKind.env, scope=scope)

        assert result is not None

    def test_variable_kind_enum(self):
        """Test WorkspaceVariableKind enum."""
        assert WorkspaceVariableKind.env.value == "env"
        assert WorkspaceVariableKind.tf.value == "tf"

    def test_value_type_enum(self):
        """Test WorkspaceValueType enum."""
        assert WorkspaceValueType.string.value == "string"
        assert WorkspaceValueType.secret.value == "secret"
