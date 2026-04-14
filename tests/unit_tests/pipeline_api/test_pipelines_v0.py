"""Unit tests for PipelinesV0Api."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.pipeline_api.pipelines_v0 import (
    PipelineV0CreateRequest,
    PipelineV0Response,
)
from harness_python_sdk.pipeline_api.pipelines_v0 import PipelinesV0Api
from harness_python_sdk.scope import Scope


class TestPipelinesV0Api:
    """Test suite for PipelinesV0Api."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(
            return_value=Scope(
                account_id="acc123", org="org123", project="proj123"
            )
        )
        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {
                    "accountIdentifier": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                }
            return "/pipeline/api/pipelines"
        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create PipelinesV0Api instance."""
        return PipelinesV0Api(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "identifier": "build_pipeline",
            "name": "Build Pipeline",
            "stages":[],
        }
        mock_client._get = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("build_pipeline", scope=scope)

        assert result.identifier == "build_pipeline"
        mock_client._get.assert_called_once()

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        response_data = {"identifier": "pipeline1", "name": "Pipeline"}
        mock_client._post = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = PipelineV0CreateRequest(
            identifier="pipeline1",
            name="Pipeline",
            stages=[],
            variables=[],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "pipeline1"
        mock_client._post.assert_called_once()

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("pipeline1", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert results == []

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("pipeline1", scope=scope)

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/pipeline/api/pipelines"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key == "pipeline"

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is True

    def test_update_success(self, api, mock_client):
        """Test successful update operation."""
        response_data = {"identifier": "pipeline1", "name": "Updated"}
        mock_client._put = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = PipelineV0CreateRequest(
            identifier="pipeline1",
            name="Updated",
            stages=[],
            variables=[],
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("pipeline1", body, scope=scope)

        assert result.name == "Updated"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = PipelineV0CreateRequest(
            identifier="p1", name="P", stages=[], variables=[]
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)
