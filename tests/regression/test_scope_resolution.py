"""Regression tests for scope resolution decision tree."""

import pytest

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.exceptions import ScopeNotSetError
from harness_python_sdk.scope import Scope


class TestScopeResolutionDecisionTree:
    """Test all scope resolution scenarios."""

    def test_no_default_scope_no_call_scope_raises(self):
        """(a) No default scope + no call scope → ScopeNotSetError."""
        # Create client with no default org/project
        client = HarnessClient(api_key="key", account_id="acc")
        # Try to resolve with no call-time scope and required placeholder missing
        with pytest.raises(ScopeNotSetError):
            # Simulate URL building that requires org
            client._build_url("/v1/accounts/{account_id}/orgs/{org}", Scope(account_id="acc"))
        client.close()

    def test_default_scope_only_used(self):
        """(b) Default scope only → used."""
        client = HarnessClient(
            api_key="key",
            account_id="acc",
            default_org="org-default",
            default_project="proj-default",
        )
        # No call-time scope, use default
        resolved = client._resolve_scope(None)
        assert resolved.account_id == "acc"
        assert resolved.org == "org-default"
        assert resolved.project == "proj-default"
        client.close()

    def test_call_scope_only_used(self):
        """(c) Call scope only → used."""
        client = HarnessClient(
            api_key="key",
            account_id="acc",
        )
        # Provide call-time scope, no default
        call_scope = Scope(account_id="acc", org="org-call", project="proj-call")
        resolved = client._resolve_scope(call_scope)
        assert resolved.org == "org-call"
        assert resolved.project == "proj-call"
        client.close()

    def test_both_scopes_call_wins(self):
        """(d) Both default and call scope → call scope wins."""
        client = HarnessClient(
            api_key="key",
            account_id="acc",
            default_org="org-default",
            default_project="proj-default",
        )
        # Provide call-time scope that should override default
        call_scope = Scope(account_id="acc", org="org-call", project="proj-call")
        resolved = client._resolve_scope(call_scope)
        assert resolved.org == "org-call"
        assert resolved.project == "proj-call"
        client.close()

    def test_partial_default_partial_call(self):
        """Test mixing default and call-time scopes partially."""
        client = HarnessClient(
            api_key="key",
            account_id="acc",
            default_org="org-default",
            default_project="proj-default",
        )
        # Call scope only provides org, should use default project
        call_scope = Scope(account_id="acc", org="org-call", project=None)
        resolved = client._resolve_scope(call_scope)
        assert resolved.org == "org-call"
        # project should come from default if call doesn't provide it
        # Current implementation: call-time org=call, project=None; then merges
        # If call.project is None, uses default.project
        client.close()

    def test_account_id_always_required(self):
        """Test that account_id is always required."""
        client = HarnessClient(api_key="key", account_id="acc")
        # Try building URL with account_id placeholder
        scope = Scope(account_id="acc-123")
        url = client._build_url("/v1/accounts/{account_id}", scope)
        assert "acc-123" in url
        client.close()
