"""Unit tests for ServicesApi."""

from unittest.mock import MagicMock

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ApiError
from harness_python_sdk.models.ng_api.services import (
    ServiceCreateRequest,
    ServiceResponse,
)
from harness_python_sdk.ng_api.services import ServicesApi
from harness_python_sdk.scope import Scope


class TestServicesApi:
    """Test suite for ServicesApi."""

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
            return "/ng/api/services"
        client._build_url = MagicMock(side_effect=build_url_side_effect)
        return client

    @pytest.fixture
    def api(self, mock_client):
        """Create ServicesApi instance."""
        return ServicesApi(mock_client)

    @pytest.fixture
    def sample_service_response(self):
        """Sample service response."""
        return {
            "identifier": "backend_service",
            "name": "Backend Service",
            "type": "NativeHelm",
            "accountIdentifier": "acc123",
            "orgIdentifier": "org123",
            "projectIdentifier": "proj123",
            "description": "Backend microservice",
            "tags": {"tier": "backend"},
            "createdAt": 1234567890000,
            "lastModifiedAt": 1234567890000,
            "yaml": "service:\n  demo: test\n"
        }

    def test_get_success(self, api, mock_client, sample_service_response):
        """Test successful get operation."""
        mock_client._get = MagicMock(return_value={"service": sample_service_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_service_response)

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.get("backend_service", scope=scope)

        assert result.identifier == "backend_service"

    def test_create_success(self, api, mock_client, sample_service_response):
        """Test successful create operation."""
        mock_client._post = MagicMock(return_value={"service": sample_service_response})
        mock_client._unwrap_response = MagicMock(return_value=sample_service_response)

        body = ServiceCreateRequest(
            identifier="backend_service",
            name="Backend Service",
            type="NativeHelm",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.create(body, scope=scope)

        assert result.identifier == "backend_service"

    def test_update_success(self, api, mock_client, sample_service_response):
        """Test successful update operation."""
        updated = sample_service_response.copy()
        updated["name"] = "Updated Backend"
        mock_client._put = MagicMock(return_value={"service": updated})
        mock_client._unwrap_response = MagicMock(return_value=updated)

        body = ServiceCreateRequest(
            identifier="backend_service",
            name="Updated Backend",
            type="NativeHelm",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.update("backend_service", body, scope=scope)

        assert result.name == "Updated Backend"

    def test_delete_success(self, api, mock_client):
        """Test successful delete operation."""
        mock_client._delete = MagicMock(return_value={"status": "SUCCESS"})

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        result = api.delete("backend_service", scope=scope)

        assert result is not None

    def test_list_success(self, api, mock_client, sample_service_response):
        """Test list operation."""
        mock_client._paginate = MagicMock(
            return_value=[sample_service_response]
        )

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 1

    def test_get_not_found(self, api, mock_client):
        """Test get with 404 error."""
        mock_client._get = MagicMock(side_effect=ApiError(404, "Not found", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.get("nonexistent", scope=scope)

    def test_create_validation_error(self, api, mock_client):
        """Test create with validation error."""
        mock_client._post = MagicMock(side_effect=ApiError(400, "Bad request", {}))

        body = ServiceCreateRequest(identifier="", name="", type="")
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.create(body, scope=scope)

    def test_delete_forbidden(self, api, mock_client):
        """Test delete with 403 error."""
        mock_client._delete = MagicMock(side_effect=ApiError(403, "Forbidden", {}))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.delete("backend_service", scope=scope)

    def test_list_multiple_pages(self, api, mock_client, sample_service_response):
        """Test list with multiple pages."""
        svc2 = sample_service_response.copy()
        svc2["identifier"] = "frontend_service"

        services = [
            sample_service_response,
            svc2,
        ]
        mock_client._paginate = MagicMock(return_value=iter(services))

        scope = Scope(account_id="acc123", org="org123", project="proj123")
        results = list(api.list(scope=scope))

        assert len(results) == 2

    def test_wrapped_body_structure(self, api):
        """Test _wrapped_body structure."""
        api._resolved_scope = Scope(
            account_id="acc123", org="org123", project="proj123"
        )
        body = ServiceCreateRequest(
            identifier="backend_service",
            name="Updated Backend",
            type="NativeHelm",
        )
        wrapped = api._wrapped_body(body)

        assert "yaml" in wrapped

    def test_update_not_found(self, api, mock_client):
        """Test update with 404 error."""
        mock_client._put = MagicMock(side_effect=ApiError(404, "Not found", {}))

        body = ServiceCreateRequest(
            identifier="backend_service",
            name="Updated Backend",
            type="NativeHelm",
        )
        scope = Scope(account_id="acc123", org="org123", project="proj123")
        with pytest.raises(ApiError):
            api.update("nonexistent", body, scope=scope)
