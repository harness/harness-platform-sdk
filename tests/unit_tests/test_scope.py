"""Unit tests for Scope."""

import pytest

from harness_platform_sdk.scope import Scope


class TestScope:
    """Test Scope functionality."""

    def test_scope_creation_with_required_fields(self):
        """Test creating Scope with only required field."""
        scope = Scope(account_id="acc-123")
        assert scope.account_id == "acc-123"
        assert scope.org is None
        assert scope.project is None

    def test_scope_creation_with_all_fields(self):
        """Test creating Scope with all fields."""
        scope = Scope(account_id="acc-123", org="org-456", project="proj-789")
        assert scope.account_id == "acc-123"
        assert scope.org == "org-456"
        assert scope.project == "proj-789"

    def test_scope_requires_account_id(self):
        """Test that Scope requires account_id."""
        with pytest.raises(ValueError):
            Scope()

    def test_scope_org_optional(self):
        """Test that Scope org is optional."""
        scope = Scope(account_id="acc")
        assert scope.org is None

    def test_scope_project_optional(self):
        """Test that Scope project is optional."""
        scope = Scope(account_id="acc")
        assert scope.project is None

    def test_scope_frozen(self):
        """Test that Scope is frozen and cannot be mutated."""
        scope = Scope(account_id="acc")
        with pytest.raises(ValueError, match="frozen"):
            scope.account_id = "new-acc"

    def test_scope_frozen_org(self):
        """Test that Scope org field is frozen."""
        scope = Scope(account_id="acc")
        with pytest.raises(ValueError, match="frozen"):
            scope.org = "new-org"

    def test_scope_frozen_project(self):
        """Test that Scope project field is frozen."""
        scope = Scope(account_id="acc")
        with pytest.raises(ValueError, match="frozen"):
            scope.project = "new-proj"

    def test_scope_equality(self):
        """Test Scope equality comparison."""
        scope1 = Scope(account_id="acc", org="org", project="proj")
        scope2 = Scope(account_id="acc", org="org", project="proj")
        assert scope1 == scope2

    def test_scope_inequality(self):
        """Test Scope inequality comparison."""
        scope1 = Scope(account_id="acc1", org="org", project="proj")
        scope2 = Scope(account_id="acc2", org="org", project="proj")
        assert scope1 != scope2

    def test_scope_hashable(self):
        """Test that Scope is hashable (frozen)."""
        scope = Scope(account_id="acc", org="org", project="proj")
        hash(scope)  # Should not raise

    def test_scope_can_be_used_in_set(self):
        """Test that Scope can be used in a set."""
        scope1 = Scope(account_id="acc", org="org", project="proj")
        scope2 = Scope(account_id="acc", org="org", project="proj")
        scope_set = {scope1, scope2}
        assert len(scope_set) == 1

    def test_scope_serialization(self):
        """Test that Scope can be serialized to dict."""
        scope = Scope(account_id="acc", org="org", project="proj")
        dumped = scope.model_dump()
        assert dumped["account_id"] == "acc"
        assert dumped["org"] == "org"
        assert dumped["project"] == "proj"

    def test_scope_none_values_serialized(self):
        """Test that None values are preserved in serialization."""
        scope = Scope(account_id="acc")
        dumped = scope.model_dump()
        assert dumped["account_id"] == "acc"
        assert dumped["org"] is None
        assert dumped["project"] is None
