"""Unit tests for Variables API."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.ng_api.variables import (
    VariableCreateRequest,
    VariableResponse,
    VariableSpec,
)
from harness_python_sdk.ng_api.variables import VariablesApi
from harness_python_sdk.scope import Scope


class TestVariablesApi:
    """Test suite for VariablesApi."""

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
            return "/ng/api/variables"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        client._unwrap_response = MagicMock(
            side_effect=lambda key_type=None, raw_data=None, scope=None: raw_data or {}
        )
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create VariablesApi instance."""
        return VariablesApi(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "identifier": "var1",
            "name": "TestVariable",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "type": "String",
            "spec": {
                "valueType": "FIXED",
                "type": "string",
                "fixedValue": "test_value",
            },
        }
        mock_client._get = MagicMock(return_value=response_data)

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.get("var1", scope=scope)

        assert result.identifier == "var1"
        assert result.name == "TestVariable"

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        response_data = {
            "identifier": "var1",
            "name": "TestVariable",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "type": "String",
            "spec": {
                "valueType": "FIXED",
                "type": "string",
                "fixedValue": "test_value",
            },
        }
        mock_client._post = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = VariableCreateRequest(
            identifier="var1",
            name="TestVariable",
            type="String",
            spec=VariableSpec(value_type="FIXED", type="string", fixed_value="test_value"),
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.create(body, scope=scope)

        assert result.identifier == "var1"
        assert result.name == "TestVariable"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.delete("var1", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client):
        """Test list operation."""
        response_data = [
            {
                "identifier": "var1",
                "name": "TestVariable1",
                "accountIdentifier": "acc123",
                "orgIdentifier": "org123",
                "projectIdentifier": "proj123",
                "type": "String",
                "spec": {
                    "valueType": "FIXED",
                    "type": "string",
                    "fixedValue": "value1",
                },
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
        assert results[0].identifier == "var1"

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
            api.delete("var1", scope=scope)

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/ng/api/variables"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key == "variable"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "variable"

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is True

    def test_update_success(self, api, mock_client):
        """Test successful update operation."""
        response_data = {
            "identifier": "var1",
            "name": "UpdatedVariable",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "type": "String",
            "spec": {
                "valueType": "FIXED",
                "type": "string",
                "fixedValue": "updated_value",
            },
        }
        mock_client._put = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = VariableCreateRequest(
            identifier="var1",
            name="UpdatedVariable",
            type="String",
            spec=VariableSpec(value_type="FIXED", type="string", fixed_value="updated_value"),
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        result = api.update("var1", body, scope=scope)

        assert result.name == "UpdatedVariable"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = VariableCreateRequest(
            identifier="var1",
            name="TestVariable",
            type="String",
            spec=VariableSpec(value_type="FIXED", type="string", fixed_value="test_value"),
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

    def test_wrapped_body(self, api):
        """Test _wrapped_body method."""
        body = VariableCreateRequest(
            identifier="var1",
            name="TestVariable",
            type="String",
            spec=VariableSpec(value_type="FIXED", type="string", fixed_value="test_value"),
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
        )
        api.resolved_scope = scope
        wrapped = api._wrapped_body(body)

        assert "variable" in wrapped
        assert wrapped["variable"]["identifier"] == "var1"

    def test_unwrapped_response(self, api):
        """Test _unwrapped_response method."""
        response_data = {
            "identifier": "var1",
            "name": "TestVariable",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "type": "String",
            "spec": {
                "valueType": "FIXED",
                "type": "string",
                "fixedValue": "test_value",
            },
        }
        result = api._unwrapped_response(response_data)

        assert isinstance(result, VariableResponse)
        assert result.identifier == "var1"
