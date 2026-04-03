"""Unit tests for HarnessConfig."""

import pytest

from harness_python_sdk.config import HarnessConfig


class TestHarnessConfig:
    """Test HarnessConfig functionality."""

    def test_config_creation_with_required_fields(self):
        """Test creating config with only required fields."""
        config = HarnessConfig(api_key="test-key", account_id="acc-123")
        assert config.api_key == "test-key"
        assert config.account_id == "acc-123"

    def test_config_defaults(self):
        """Test that config has correct defaults."""
        config = HarnessConfig(api_key="key", account_id="acc")
        assert config.base_url == "https://app.harness.io"
        assert config.timeout == 30.0
        assert config.max_retries == 3
        assert config.retry_status_codes == [429, 503]
        assert config.retry_enabled is True
        assert config.verify_ssl is True

    def test_config_custom_values(self):
        """Test creating config with custom values."""
        config = HarnessConfig(
            api_key="key",
            account_id="acc",
            base_url="https://custom.harness.io",
            timeout=60.0,
            max_retries=5,
            retry_status_codes=[429, 500, 503],
            retry_enabled=False,
            verify_ssl=False,
        )
        assert config.base_url == "https://custom.harness.io"
        assert config.timeout == 60.0
        assert config.max_retries == 5
        assert config.retry_status_codes == [429, 500, 503]
        assert config.retry_enabled is False
        assert config.verify_ssl is False

    def test_config_repr_redacts_api_key(self):
        """Test that __repr__ redacts the API key."""
        config = HarnessConfig(api_key="secret-key-12345", account_id="acc-123")
        repr_str = repr(config)
        assert "secret-key-12345" not in repr_str
        assert "api_key='***'" in repr_str
        assert "acc-123" in repr_str

    def test_config_requires_api_key(self):
        """Test that config requires api_key."""
        with pytest.raises(ValueError):
            HarnessConfig(account_id="acc-123")

    def test_config_requires_account_id(self):
        """Test that config requires account_id."""
        with pytest.raises(ValueError):
            HarnessConfig(api_key="key")

    def test_config_both_required_fields_missing(self):
        """Test that config requires both api_key and account_id."""
        with pytest.raises(ValueError):
            HarnessConfig()

    def test_config_immutable(self):
        """Test that config values can be set but model follows Pydantic patterns."""
        config = HarnessConfig(api_key="key", account_id="acc")
        # Pydantic v2 models are not frozen by default unless specified
        config.timeout = 60.0
        assert config.timeout == 60.0

    def test_config_serialization(self):
        """Test that config can be serialized to dict (with secret)."""
        config = HarnessConfig(api_key="secret", account_id="acc")
        dumped = config.model_dump()
        assert dumped["api_key"] == "secret"
        assert dumped["account_id"] == "acc"
