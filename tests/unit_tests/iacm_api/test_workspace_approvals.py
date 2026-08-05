"""Unit tests for Workspace Approvals IACM API."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.iacm_api.workspace_approvals import WorkspaceApprovalsApi
from harness_python_sdk.models.iacm_api.workspace_approvals import (
    WorkspaceApprovalCreateRequest,
    WorkspaceApprovalListResponse,
    WorkspaceApprovalResponse,
    WorkspaceApprovalStatus,
)
from harness_python_sdk.scope import Scope


class TestWorkspaceApprovalsApi:
    """Test suite for WorkspaceApprovalsApi."""

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
            return "/iacm/api/orgs/org123/projects/proj123/approvals"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        client._unwrap_response = MagicMock(
            side_effect=lambda key_type=None, raw_data=None, scope=None: raw_data or {}
        )
        client._display_payload = MagicMock()
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create WorkspaceApprovalsApi instance."""
        return WorkspaceApprovalsApi(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "id": "approval1",
            "workspace_id": "ws1",
            "pipeline_stage_id": "stage1",
            "pipeline_execution_id": "exec1",
            "status": "pending",
            "created": 1609459200000,
        }
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("approval1", scope=scope)

        assert isinstance(result, WorkspaceApprovalResponse)

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        response_data = [
            {
                "id": "approval1",
                "workspace_id": "ws1",
                "pipeline_stage_id": "stage1",
                "pipeline_execution_id": "exec1",
                "status": "pending",
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "created": 1609459200000,
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
        assert isinstance(results[0], WorkspaceApprovalListResponse)

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

    def test_update_approved(self, api, mock_client):
        """Test successful update to approved status."""
        mock_client._put = MagicMock(return_value={})

        body = WorkspaceApprovalCreateRequest(
            identifier="approval1",
            status=WorkspaceApprovalStatus.approved,
            actioned_by="user123",
            actioned_by_email="user@example.com",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.update("approval1", body, scope=scope)

        assert result.status == WorkspaceApprovalStatus.approved

    def test_update_rejected(self, api, mock_client):
        """Test successful update to rejected status."""
        mock_client._put = MagicMock(return_value={})

        body = WorkspaceApprovalCreateRequest(
            identifier="approval1",
            status=WorkspaceApprovalStatus.rejected,
            actioned_by="user123",
            actioned_by_email="user@example.com",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.update("approval1", body, scope=scope)

        assert result.status == WorkspaceApprovalStatus.rejected

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

    def test_approval_status_enum(self):
        """Test WorkspaceApprovalStatus enum."""
        assert WorkspaceApprovalStatus.approved.value == "approved"
        assert WorkspaceApprovalStatus.rejected.value == "rejected"
        assert WorkspaceApprovalStatus.pending.value == "pending"
        assert WorkspaceApprovalStatus.unknown.value == "unknown"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.delete("approval1", scope=scope)

        assert result is not None
