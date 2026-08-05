"""Unit tests for ProjectsApi."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.ng_api.projects import (
    ProjectCreateRequest,
    ProjectResponse,
)
from harness_python_sdk.ng_api.projects import ProjectsApi
from harness_python_sdk.scope import Scope


class TestProjectsApi:
    """Test suite for ProjectsApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(return_value=Scope(account_id="acc123", org="org123"))

        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {"accountIdentifier": "acc123", "orgIdentifier": "org123"}
            return "/ng/api/projects"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create ProjectsApi instance with mock client."""
        return ProjectsApi(mock_client)

    @pytest.fixture
    def sample_project_response(self):
        """Sample project response."""
        return {
            "identifier": "proj123",
            "name": "Test Project",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "description": "Test project",
            "tags": {"env": "test"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_init(self, mock_client):
        """Test ProjectsApi initialization."""
        api = ProjectsApi(mock_client)
        assert api._client == mock_client

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/ng/api/projects"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "project"

    def test_get_success(self, api, mock_client, sample_project_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"project": sample_project_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_project_response)

        scope = Scope(account_id="acc123", org="org123")
        result = api.get("proj123", scope=scope)

        assert result.identifier == "proj123"
        mock_client._get.assert_called_once()

    def test_get_not_found(self, api, mock_client):
        """Test get operation with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_create_success(self, api, mock_client, sample_project_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"project": sample_project_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_project_response)

        body = ProjectCreateRequest(
            identifier="proj123",
            name="Test Project",
            description="Test",
        )
        scope = Scope(account_id="acc123", org="org123")
        result = api.create(body, scope=scope)

        assert result.identifier == "proj123"

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = ProjectCreateRequest(identifier="proj123", name="Test")
        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_update_success(self, api, mock_client, sample_project_response):
        """Test successful update operation."""
        updated_response = sample_project_response.copy()
        updated_response["name"] = "Updated"
        mock_client._put = MagicMock(return_value={"project": updated_response})
        mock_client._unwrap_response = MagicMock(return_value=updated_response)

        body = ProjectCreateRequest(identifier="proj123", name="Updated")
        scope = Scope(account_id="acc123", org="org123")
        result = api.update("proj123", body, scope=scope)

        assert result.name == "Updated"

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = ProjectCreateRequest(identifier="proj123", name="Updated")
        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123")
        result = api.delete("proj123", scope=scope)

        assert result is not None

    def test_delete_not_found(self, api, mock_client):
        """Test delete with 404 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123")
        with pytest.raises(ApiError):
            api.delete("nonexistent", scope=scope)

    def test_list_single_page(self, api, mock_client, sample_project_response):
        """Test list operation with single page."""
        mock_client._paginate = MagicMock(
            return_value=iter([ProjectResponse(**sample_project_response)])
        )

        scope = Scope(account_id="acc123", org="org123")
        results = list(api.list(scope=scope))

        assert len(results) == 1
        assert results[0].identifier == "proj123"

    def test_list_multiple_pages(self, api, mock_client, sample_project_response):
        """Test list operation with multiple pages."""
        proj2 = sample_project_response.copy()
        proj2["identifier"] = "proj456"
        proj2["name"] = "Project 2"

        projects = [
            ProjectResponse(**sample_project_response),
            ProjectResponse(**proj2),
        ]
        mock_client._paginate = MagicMock(return_value=iter(projects))

        scope = Scope(account_id="acc123", org="org123")
        results = list(api.list(scope=scope))

        assert len(results) == 2
        assert results[0].identifier == "proj123"
        assert results[1].identifier == "proj456"

    def test_list_empty(self, api, mock_client):
        """Test list operation with no results."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123")
        results = list(api.list(scope=scope))

        assert len(results) == 0

    def test_wrapped_body_injects_scope(self, api):
        """Test _wrapped_body injects scope identifiers."""
        api._resolved_scope = Scope(account_id="acc123", org="org123")
        body = ProjectCreateRequest(identifier="proj123", name="Test")
        wrapped = api._wrapped_body(body)

        assert wrapped["project"]["accountIdentifier"] == "acc123"
        assert wrapped["project"]["orgIdentifier"] == "org123"

    def test_resolved_scope_property(self, api, mock_client):
        """Test resolved_scope property setter."""
        scope = Scope(account_id="acc123", org="org123")
        api.resolved_scope = scope

        assert api.resolved_scope.account_id == "acc123"
        assert api.resolved_scope.org == "org123"

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(account_id="acc123", org="org123")
        result = api.get("proj123", scope=scope)

        assert result == {}
