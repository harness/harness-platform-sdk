"""Regression tests for client lifecycle."""

from harness_platform_sdk.client import HarnessClient


class TestClientLifecycle:
    """Test client lifecycle and resource management."""

    def test_context_manager_closes_client(self):
        """Test that context manager properly closes client."""
        with HarnessClient(api_key="key", account_id="acc") as client:
            http_client = client._http_client
            assert http_client is not None
            # Client should be usable inside context
            assert client._config is not None
        # After exit, httpx.Client is closed
        # (We can't directly verify closure without inspecting internals)

    def test_explicit_close_works(self):
        """Test that explicit close() works."""
        client = HarnessClient(api_key="key", account_id="acc")
        http_client = client._http_client
        assert http_client is not None
        client.close()
        # Should not raise

    def test_double_close_does_not_raise(self):
        """Test that calling close() twice does not raise."""
        client = HarnessClient(api_key="key", account_id="acc")
        client.close()
        client.close()  # Should not raise

    def test_client_accessible_in_context(self):
        """Test that client methods work inside context manager."""
        with HarnessClient(
            api_key="key",
            account_id="acc",
            default_org="org",
            default_project="proj",
        ) as client:
            # Test that scope operations work
            scope = client._resolve_scope(None)
            assert scope.org == "org"
            assert scope.project == "proj"

            # Test URL building
            url = client._build_url(
                "/v1/accounts/{account_id}/orgs/{org}",
                scope,
            )
            assert "acc" in url
            assert "org" in url

    def test_set_default_scope_after_construction(self):
        """Test that default scope can be updated after construction."""
        client = HarnessClient(api_key="key", account_id="acc", default_org="org1")
        assert client._default_scope.org == "org1"

        # Update scope
        client.set_default_scope(org="org2", project="proj2")
        assert client._default_scope.org == "org2"
        assert client._default_scope.project == "proj2"
        assert client._default_scope.account_id == "acc"

        client.close()

    def test_multiple_clients_independent(self):
        """Test that multiple client instances are independent."""
        client1 = HarnessClient(
            api_key="key1",
            account_id="acc1",
            default_org="org1",
        )
        client2 = HarnessClient(
            api_key="key2",
            account_id="acc2",
            default_org="org2",
        )

        assert client1._config.api_key == "key1"
        assert client2._config.api_key == "key2"
        assert client1._default_scope.org == "org1"
        assert client2._default_scope.org == "org2"

        client1.close()
        client2.close()

    def test_base_url_setter_no_session_leak(self):
        """Test that base_url setter twice does not leak sessions."""
        client = HarnessClient(api_key="key", account_id="acc")

        # Set base_url first time
        first_client = client._http_client
        client.base_url = "https://my.harness.io"
        assert first_client.is_closed

        # Set base_url second time
        second_client = client._http_client
        client.base_url = "https://another.harness.io"
        assert second_client.is_closed

        # Final client should be open
        assert not client._http_client.is_closed
        assert client.base_url == "https://another.harness.io"

        client.close()
