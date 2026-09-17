"""Unit tests for InfrastructuresApi."""

from unittest.mock import MagicMock

import pytest

from harness_platform_sdk.client import HarnessClient
from harness_platform_sdk.exceptions import ApiError
from harness_platform_sdk.models.ng_api.infrastructures import (
    InfrastructureCreateRequest,
    InfrastructureResponse,
)
from harness_platform_sdk.ng_api.infrastructures import InfrastructuresApi
from harness_platform_sdk.scope import Scope


class TestInfrastructuresApi:
    """Test suite for InfrastructuresApi."""

    @pytest.fixture
    def mock_client(self):
        """Create mock HarnessClient."""
        client = MagicMock(spec=HarnessClient)
        client._resolve_scope = MagicMock(
            return_value=Scope(account_id="acc123", org="org123", project="proj123")
        )

        def build_url_side_effect(*args, **kwargs):
            if kwargs.get("is_params"):
                return {
                    "accountIdentifier": "acc123",
                    "orgIdentifier": "org123",
                    "projectIdentifier": "proj123",
                }
            return "/ng/api/infrastructures"

        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create InfrastructuresApi instance."""
        return InfrastructuresApi(mock_client)

    @pytest.fixture
    def sample_infra_response(self):
        """Sample infrastructure response."""
        return {
            "identifier": "k8s_infra",
            "name": "Kubernetes Infrastructure",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "environmentIdentifier": "env123",
            "description": "K8s cluster",
            "type": "KubernetesDirect",
            "deployment_type": "Kubernetes",
            "spec": {
                "connectorRef": "<+input>",
                "namespace": "<+input>",
                "releaseName": "release-<+INFRA_KEY_SHORT_ID>",
            },
            "tags": {"cloud": "aws"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
        }

    def test_get_success(self, api, mock_client, sample_infra_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"infrastructure": sample_infra_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_infra_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("k8s_infra", environment_identifier="env123", scope=scope)

        assert result.identifier == "k8s_infra"

    def test_create_success(self, api, mock_client, sample_infra_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"infrastructure": sample_infra_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_infra_response)

        body = InfrastructureCreateRequest(
            identifier="k8s_infra",
            name="Kubernetes Infrastructure",
            environment_identifier="env123",
            type="KubernetesDirect",
            deployment_type="Kubernetes",
            spec={
                "connectorRef": "<+input>",
                "namespace": "<+input>",
                "releaseName": "release-<+INFRA_KEY_SHORT_ID>",
            },
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "k8s_infra"

    def test_update_success(self, api, mock_client, sample_infra_response):
        """Test successful update operation."""
        updated = sample_infra_response.copy()
        updated["name"] = "Updated K8s"
        mock_client._put = MagicMock(return_value={"infrastructure": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = InfrastructureCreateRequest(
            identifier="k8s_infra",
            name="Updated K8s",
            environment_identifier="env123",
            type="KubernetesDirect",
            deployment_type="Kubernetes",
            spec={
                "connectorRef": "<+input>",
                "namespace": "<+input>",
                "releaseName": "release-<+INFRA_KEY_SHORT_ID>",
            },
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("k8s_infra", body, scope=scope)

        assert result.name == "Updated K8s"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("k8s_infra", environment_identifier="env123", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_infra_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(return_value=iter([sample_infra_response]))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(environment_identifier="env123", scope=scope))

        assert len(results) == 1

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("nonexistent", environment_identifier="env123", scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("k8s_infra", environment_identifier="env123", scope=scope)

    def test_list_multiple_pages(self, api, mock_client, sample_infra_response):
        """Test list with multiple pages."""
        infra2 = sample_infra_response.copy()
        infra2["identifier"] = "infra2"

        infras = [
            sample_infra_response,
            infra2,
        ]
        mock_client._paginate = MagicMock(return_value=iter(infras))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(environment_identifier="env123", scope=scope))

        assert len(results) == 2

    def test_wrapped_body_structure(self, api):
        """Test _wrapped_body structure."""
        api._resolved_scope = Scope(account_id="acc123", org="org123", project="proj123")
        body = InfrastructureCreateRequest(
            identifier="infra1",
            name="Test",
            environment_identifier="env123",
            type="KubernetesDirect",
            deployment_type="Kubernetes",
            spec={},
        )
        wrapped = api._wrapped_body(body)

        assert "yaml" in wrapped
        assert "infrastructureDefinition" in wrapped["yaml"]

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = InfrastructureCreateRequest(
            identifier="",
            name="",
            environment_identifier="",
            type="",
            deployment_type="",
            spec={},
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)
