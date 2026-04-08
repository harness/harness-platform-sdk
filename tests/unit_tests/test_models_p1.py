"""
Unit tests for P1 domain models.

Verifies that all P1 models:
- Are instances of HarnessModel
- Support extra fields (forward compatibility)
- Support populate_by_name (camelCase → snake_case mapping)
"""

import pytest

from harness_python_sdk.base_model import HarnessModel
from harness_python_sdk.models import (
    ConnectorCreateRequest,
    ConnectorResponse,
    ConnectorUpdateRequest,
    InfrastructureCreateRequest,
    InfrastructureResponse,
    InfrastructureUpdateRequest,
    PipelineCreateRequest,
    PipelineResponse,
    PipelineUpdateRequest,
    SecretCreateRequest,
    SecretResponse,
    SecretUpdateRequest,
)


class TestPipelineModels:
    """Tests for Pipeline models."""

    def test_pipeline_response_is_harness_model(self):
        """PipelineResponse is a HarnessModel."""
        payload = {"identifier": "my-pipeline", "name": "My Pipeline"}
        model = PipelineResponse(**payload)
        assert isinstance(model, HarnessModel)

    def test_pipeline_response_extra_allow(self):
        """PipelineResponse allows extra fields."""
        payload = {
            "identifier": "my-pipeline",
            "name": "My Pipeline",
            "extra_field": "extra_value",
        }
        model = PipelineResponse(**payload)
        assert model.extra_field == "extra_value"

    def test_pipeline_response_populate_by_name(self):
        """PipelineResponse supports populate_by_name."""
        payload = {
            "identifier": "my-pipeline",
            "name": "My Pipeline",
            "pipelineYaml": "some yaml",
        }
        model = PipelineResponse(**payload)
        assert model.pipeline_yaml == "some yaml"

    def test_pipeline_create_request(self):
        """PipelineCreateRequest instantiation."""
        payload = {
            "identifier": "my-pipeline",
            "name": "My Pipeline",
            "pipeline_yaml": "some yaml",
        }
        model = PipelineCreateRequest(**payload)
        assert isinstance(model, HarnessModel)
        assert model.identifier == "my-pipeline"

    def test_pipeline_update_request(self):
        """PipelineUpdateRequest instantiation."""
        payload = {
            "identifier": "my-pipeline",
            "name": "My Pipeline",
            "pipeline_yaml": "some yaml",
        }
        model = PipelineUpdateRequest(**payload)
        assert isinstance(model, HarnessModel)


class TestConnectorModels:
    """Tests for Connector models."""

    def test_connector_response_is_harness_model(self):
        """ConnectorResponse is a HarnessModel."""
        payload = {"identifier": "my-connector", "name": "My Connector"}
        model = ConnectorResponse(**payload)
        assert isinstance(model, HarnessModel)

    def test_connector_response_extra_allow(self):
        """ConnectorResponse allows extra fields."""
        payload = {
            "identifier": "my-connector",
            "name": "My Connector",
            "extra_field": "extra_value",
        }
        model = ConnectorResponse(**payload)
        assert model.extra_field == "extra_value"

    def test_connector_response_populate_by_name(self):
        """ConnectorResponse supports populate_by_name with field aliases."""
        # Test with camelCase alias for governance_metadata
        payload = {
            "identifier": "my-connector",
            "name": "My Connector",
            "governanceMetadata": {"policy": "test"},
        }
        model = ConnectorResponse(**payload)
        assert model.governance_metadata == {"policy": "test"}

    def test_connector_create_request(self):
        """ConnectorCreateRequest instantiation."""
        payload = {
            "identifier": "my-connector",
            "name": "My Connector",
            "spec": {"type": "Git"},
        }
        model = ConnectorCreateRequest(**payload)
        assert isinstance(model, HarnessModel)

    def test_connector_update_request(self):
        """ConnectorUpdateRequest instantiation."""
        payload = {
            "identifier": "my-connector",
            "name": "My Connector",
            "spec": {"type": "Git"},
        }
        model = ConnectorUpdateRequest(**payload)
        assert isinstance(model, HarnessModel)


class TestSecretModels:
    """Tests for Secret models."""

    def test_secret_response_is_harness_model(self):
        """SecretResponse is a HarnessModel."""
        payload = {"identifier": "my-secret", "name": "My Secret"}
        model = SecretResponse(**payload)
        assert isinstance(model, HarnessModel)

    def test_secret_response_extra_allow(self):
        """SecretResponse allows extra fields."""
        payload = {
            "identifier": "my-secret",
            "name": "My Secret",
            "extra_field": "extra_value",
        }
        model = SecretResponse(**payload)
        assert model.extra_field == "extra_value"

    def test_secret_response_populate_by_name(self):
        """SecretResponse supports populate_by_name."""
        payload = {
            "identifier": "my-secret",
            "name": "My Secret",
            "governanceMetadata": {"policy": "value"},
        }
        model = SecretResponse(**payload)
        assert model.governance_metadata == {"policy": "value"}

    def test_secret_create_request(self):
        """SecretCreateRequest instantiation."""
        payload = {
            "identifier": "my-secret",
            "name": "My Secret",
            "spec": {"type": "SecretText"},
        }
        model = SecretCreateRequest(**payload)
        assert isinstance(model, HarnessModel)

    def test_secret_update_request(self):
        """SecretUpdateRequest instantiation."""
        payload = {
            "identifier": "my-secret",
            "name": "My Secret",
            "spec": {"type": "SecretText"},
        }
        model = SecretUpdateRequest(**payload)
        assert isinstance(model, HarnessModel)


class TestInfrastructureModels:
    """Tests for Infrastructure models."""

    def test_infrastructure_response_is_harness_model(self):
        """InfrastructureResponse is a HarnessModel."""
        payload = {
            "identifier": "my-infra",
            "name": "My Infrastructure",
            "type": "Kubernetes",
        }
        model = InfrastructureResponse(**payload)
        assert isinstance(model, HarnessModel)

    def test_infrastructure_response_extra_allow(self):
        """InfrastructureResponse allows extra fields."""
        payload = {
            "identifier": "my-infra",
            "name": "My Infrastructure",
            "type": "Kubernetes",
            "extra_field": "extra_value",
        }
        model = InfrastructureResponse(**payload)
        assert model.extra_field == "extra_value"

    def test_infrastructure_response_populate_by_name(self):
        """InfrastructureResponse supports populate_by_name."""
        payload = {
            "identifier": "my-infra",
            "name": "My Infrastructure",
            "type": "Kubernetes",
            "harnessVersion": "1.0",
        }
        model = InfrastructureResponse(**payload)
        assert model.harness_version == "1.0"

    def test_infrastructure_create_request(self):
        """InfrastructureCreateRequest instantiation."""
        payload = {
            "identifier": "my-infra",
            "name": "My Infrastructure",
            "type": "Kubernetes",
            "environment": "prod",
        }
        model = InfrastructureCreateRequest(**payload)
        assert isinstance(model, HarnessModel)

    def test_infrastructure_update_request(self):
        """InfrastructureUpdateRequest instantiation."""
        payload = {
            "identifier": "my-infra",
            "name": "My Infrastructure",
            "type": "Kubernetes",
            "environment": "prod",
        }
        model = InfrastructureUpdateRequest(**payload)
        assert isinstance(model, HarnessModel)


class TestAllModelsInheritFromHarnessModel:
    """Verify all 12 P1 models inherit from HarnessModel."""

    @pytest.mark.parametrize(
        "model_class",
        [
            PipelineResponse,
            PipelineCreateRequest,
            PipelineUpdateRequest,
            ConnectorResponse,
            ConnectorCreateRequest,
            ConnectorUpdateRequest,
            SecretResponse,
            SecretCreateRequest,
            SecretUpdateRequest,
            InfrastructureResponse,
            InfrastructureCreateRequest,
            InfrastructureUpdateRequest,
        ],
    )
    def test_model_inherits_from_harness_model(self, model_class):
        """All P1 model classes inherit from HarnessModel."""
        assert issubclass(model_class, HarnessModel)
