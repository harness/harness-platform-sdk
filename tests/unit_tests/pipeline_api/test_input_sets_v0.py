"""Unit tests for InputSetsV0Api."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.pipeline_api.input_sets_v0 import (
    InputSetV0CreateRequest,
    InputSetV0Response,
)
from harness_python_sdk.pipeline_api.input_sets_v0 import InputSetsV0Api
from harness_python_sdk.scope import Scope


class TestInputSetsV0Api:
    """Test suite for InputSetsV0Api."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._default_scope = MagicMock(account_id="acc123")
        client._resolve_scope = MagicMock(
            return_value=Scope(
                account_id="acc123",
                org="org123",
                project="proj123",
                pipeline="pipe1",
            )
        )

        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {
                    "accountIdentifier": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                    "pipelineIdentifier": "pipe1",
                }
            return "/pipeline/api/inputSets"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create InputSetsV0Api instance."""
        return InputSetsV0Api(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {"identifier": "input1", "name": "Input Set"}
        response_data.update(
            {
                "accountIdentifier": "acc123",
                "orgIdentifier": "org123",
                "projectIdentifier": "proj123",
                "pipelineIdentifier": "pipe1",
            }
        )
        mock_client._get = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.get("input1", "pipe1", scope=scope)

        assert result.identifier == "input1"

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        response_data = {"identifier": "input1", "name": "Input Set"}
        mock_client._post = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = InputSetV0CreateRequest(
            identifier="input1",
            name="Input Set",
            pipeline_identifier="pipe1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.create(body, scope=scope)

        assert result.identifier == "input1"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.delete("input1", "pipe1", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        results = list(api.list("pipe1", scope=scope))

        assert results == []

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.get("nonexistent", "pipe1", scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.delete("input1", "pipe1", scope=scope)

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/pipeline/api/inputSets"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key == "inputSet"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "inputSet"

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is True

    def test_update_success(self, api, mock_client):
        """Test successful update operation."""
        response_data = {"identifier": "input1", "name": "Updated"}
        mock_client._put = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = InputSetV0CreateRequest(
            identifier="input1",
            name="Updated",
            pipeline_identifier="pipe1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.update("input1", body, scope=scope)

        assert result.name == "Updated"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = InputSetV0CreateRequest(identifier="i1", name="I", pipeline_identifier="pipe1")
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_get_forbidden(self, api, mock_client):
        """Test get with 403 error."""
        mock_client._get = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.get("input1", "pipe1", scope=scope)

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = InputSetV0CreateRequest(
            identifier="input1",
            name="Updated",
            pipeline_identifier="pipe1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)

    def test_update_forbidden(self, api, mock_client):
        """Test update with 403 error."""
        mock_client._put = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        body = InputSetV0CreateRequest(
            identifier="input1",
            name="Updated",
            pipeline_identifier="pipe1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.update("input1", body, scope=scope)

    def test_delete_not_found(self, api, mock_client):
        """Test delete with 404 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.delete("nonexistent", "pipe1", scope=scope)

    def test_list_with_search_term(self, api, mock_client):
        """Test list with search term parameter."""
        mock_client._paginate = MagicMock(return_value=iter([]))

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        results = list(api.list("pipe1", scope=scope, searchTerm="input"))

        assert results == []
        mock_client._paginate.assert_called_once()

    def test_resolved_scope_property(self, api, mock_client):
        """Test resolved_scope property setter."""
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        api.resolved_scope = scope

        assert api.resolved_scope.account_id == "acc123"
        assert api.resolved_scope.org == "org123"
        assert api.resolved_scope.project == "proj123"
        mock_client._resolve_scope.assert_called()

    def test_default_params_property(self, api, mock_client):
        """Test default_params property."""
        mock_client._build_url = MagicMock(
            return_value="accountIdentifier=acc123&orgIdentifier=org123&projectIdentifier=proj123&pipelineIdentifier=pipe1"
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        api.resolved_scope = scope

        params = api.default_params
        assert params is not None

    def test_wrapped_body_wraps_inputSet(self, api, mock_client):
        """Test _wrapped_body wraps input set properly."""
        api._resolved_scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        body = InputSetV0CreateRequest(
            identifier="input1",
            name="Input Set",
            pipeline_identifier="pipe1",
        )
        wrapped = api._wrapped_body(body)

        assert "inputSet" in wrapped
        assert wrapped["inputSet"]["identifier"] == "input1"

    def test_get_empty_response(self, api, mock_client):
        """Test get with empty response."""
        mock_client._get = MagicMock(return_value=None)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.get("input1", "pipe1", scope=scope)

        assert result == {}

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict (409) error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = InputSetV0CreateRequest(
            identifier="input1",
            name="Input Set",
            pipeline_identifier="pipe1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.create(body, scope=scope)
