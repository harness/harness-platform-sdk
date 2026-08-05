"""Unit tests for Workspace Default Pipelines IACM API."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.iacm_api.workspace_default_pipelines import (
    WorkspaceDefaultPipelinesApi,
)
from harness_python_sdk.models.iacm_api.workspace_default_pipelines import (
    WorkspaceDefaultPipelineCreateRequest,
    WorkspaceDefaultPipelineOperation,
    WorkspaceDefaultPipelineProvisioner,
    WorkspaceDefaultPipelineResponse,
)
from harness_python_sdk.scope import Scope


class TestWorkspaceDefaultPipelinesApi:
    """Test suite for WorkspaceDefaultPipelinesApi."""

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
                    "workspace": "ws1",
                }
            return "/iacm/api/orgs/org123/projects/proj123/settings/default-pipelines"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create WorkspaceDefaultPipelinesApi instance."""
        return WorkspaceDefaultPipelinesApi(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation with operation filter."""
        response_data = [
            {
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "pipeline": "pipe1",
                "workspace": "ws1",
                "operation": "plan",
                "updated": 1609459200000,
            },
            {
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "pipeline": "pipe2",
                "workspace": "ws1",
                "operation": "apply",
                "updated": 1609459200000,
            },
        ]
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("ws1", WorkspaceDefaultPipelineOperation.plan, scope=scope)

        assert isinstance(result, WorkspaceDefaultPipelineResponse)
        assert result.operation == WorkspaceDefaultPipelineOperation.plan

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        response_data = [
            {
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "pipeline": "pipe1",
                "workspace": "ws1",
                "operation": "plan",
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
        assert results[0].workspace_identifier == "ws1"

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        with pytest.raises(ApiError):
            api.get("ws1", WorkspaceDefaultPipelineOperation.plan, scope=scope)

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
        response_data = {
            "account": "acc123",
            "org": "org123",
            "project": "proj123",
            "pipeline": "pipe1",
            "workspace": "ws1",
            "operation": "apply",
            "updated": 1609459200000,
        }
        mock_client._put = MagicMock(return_value=response_data)

        body = WorkspaceDefaultPipelineCreateRequest(
            account_identifier="acc123",
            org_identifier="org123",
            project_identifier="proj123",
            pipeline_identifier="pipe1",
            workspace_identifier="ws1",
            provisioner=WorkspaceDefaultPipelineProvisioner.terraform,
            operation=WorkspaceDefaultPipelineOperation.apply,
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.update(body, scope=scope)

        assert result.operation == WorkspaceDefaultPipelineOperation.apply

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

    def test_get_empty_result(self, api, mock_client):
        """Test get with no matching operation."""
        response_data = [
            {
                "account": "acc123",
                "org": "org123",
                "project": "proj123",
                "pipeline": "pipe1",
                "workspace": "ws1",
                "operation": "plan",
            }
        ]
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("ws1", WorkspaceDefaultPipelineOperation.apply, scope=scope)

        assert result == {}

    def test_operation_enum(self):
        """Test WorkspaceDefaultPipelineOperation enum."""
        assert WorkspaceDefaultPipelineOperation.plan.value == "plan"
        assert WorkspaceDefaultPipelineOperation.apply.value == "apply"
        assert WorkspaceDefaultPipelineOperation.destroy.value == "destroy"
        assert WorkspaceDefaultPipelineOperation.drift.value == "drift"

    def test_provisioner_enum(self):
        """Test WorkspaceDefaultPipelineProvisioner enum."""
        assert WorkspaceDefaultPipelineProvisioner.terraform.value == "terraform"
        assert WorkspaceDefaultPipelineProvisioner.opentofu.value == "opentofu"
