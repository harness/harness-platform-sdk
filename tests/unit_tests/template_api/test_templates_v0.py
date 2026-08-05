"""Unit tests for TemplatesV0Api."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.template_api.templates_v0 import (
    TemplateV0CreateRequest,
    TemplateV0Response,
)
from harness_python_sdk.scope import Scope
from harness_python_sdk.template_api.templates_v0 import TemplatesV0Api


class TestTemplatesV0Api:
    """Test suite for TemplatesV0Api."""

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
            return "/template/api/templates"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create TemplatesV0Api instance."""
        return TemplatesV0Api(mock_client)

    def test_get_success(self, api, mock_client):
        """Test successful get operation."""
        response_data = {
            "identifier": "trigger1",
            "name": "Updated",
            "template_entity_type": "Step",
            "version": 0,
            "version_label": "v1",
        }
        response_data.update(
            {
                "accountIdentifier": "acc123",
                "orgIdentifier": "org123",
                "projectIdentifier": "proj123",
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
        result = api.get("trigger1", scope=scope)

        assert result.identifier == "trigger1"

    def test_create_success(self, api, mock_client):
        """Test successful create operation."""
        response_data = {
            "identifier": "trigger1",
            "name": "Updated",
            "template_entity_type": "Step",
            "version": 0,
            "version_label": "v1",
        }
        mock_client._post = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = TemplateV0CreateRequest(
            identifier="trigger1",
            name="Webhook Template",
            template_entity_type="Step",
            template_spec={
                "spec": {
                    "delegateSelectors": [],
                    "environmentVariables": [],
                    "executionTarget": {},
                    "outputVariables": [],
                    "shell": "Bash",
                    "source": {"spec": {"script": 'echo "hello"'}, "type": "Inline"},
                },
                "timeout": "10m",
                "type": "ShellScript",
            },
            version_label="v1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.create(body, scope=scope)

        assert result.identifier == "trigger1"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.delete("trigger1", "pipe1", scope=scope)

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
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.delete("trigger1", "pipe1", scope=scope)

    def test_root_api_path(self, api):
        """Test root_api_path property."""
        assert api.root_api_path == "/template/api/templates"

    def test_wrap_key(self, api):
        """Test wrap_key property."""
        assert api.wrap_key == "template"

    def test_unwrap_key(self, api):
        """Test unwrap_key property."""
        assert api.unwrap_key == "templateResponseDTO"

    def test_should_wrap(self, api):
        """Test should_wrap property."""
        assert api.should_wrap is True

    def test_update_success(self, api, mock_client):
        """Test successful update operation."""
        response_data = {
            "identifier": "trigger1",
            "name": "Updated",
            "template_entity_type": "Step",
            "version": 0,
            "version_label": "v1",
        }
        mock_client._put = MagicMock(return_value=response_data)
        mock_client._unwrap_response = MagicMock(return_value=response_data)

        body = TemplateV0CreateRequest(
            identifier="trigger1",
            name="Updated",
            template_entity_type="Step",
            template_spec={
                "spec": {
                    "delegateSelectors": [],
                    "environmentVariables": [],
                    "executionTarget": {},
                    "outputVariables": [],
                    "shell": "Bash",
                    "source": {"spec": {"script": 'echo "hello"'}, "type": "Inline"},
                },
                "timeout": "10m",
                "type": "ShellScript",
            },
            version_label="v1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        result = api.update("trigger1", body, scope=scope)

        assert result.name == "Updated"

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = TemplateV0CreateRequest(
            identifier="t1",
            name="T",
            template_entity_type="Step",
            template_spec={
                "spec": {
                    "delegateSelectors": [],
                    "environmentVariables": [],
                    "executionTarget": {},
                    "outputVariables": [],
                    "shell": "Bash",
                    "source": {"spec": {"script": 'echo "hello"'}, "type": "Inline"},
                },
                "timeout": "10m",
                "type": "ShellScript",
            },
            version_label="v1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
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
            pipeline="pipe1",
        )
        results = list(api.list("pipe1", scope=scope))

        assert len(results) == 0

    def test_create_conflict(self, api, mock_client):
        """Test create with conflict error."""
        mock_client._post = MagicMock(side_effect=ApiError(409, "Conflict", {}))

        body = TemplateV0CreateRequest(
            identifier="trigger1",
            name="Template",
            template_entity_type="Step",
            template_spec={
                "spec": {
                    "delegateSelectors": [],
                    "environmentVariables": [],
                    "executionTarget": {},
                    "outputVariables": [],
                    "shell": "Bash",
                    "source": {"spec": {"script": 'echo "hello"'}, "type": "Inline"},
                },
                "timeout": "10m",
                "type": "ShellScript",
            },
            version_label="v1",
        )
        scope = Scope(
            account_id="acc123",
            org="org123",
            project="proj123",
            pipeline="pipe1",
        )
        with pytest.raises(ApiError):
            api.create(body, scope=scope)
