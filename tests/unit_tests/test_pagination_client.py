"""Unit tests for client pagination."""

from pytest_httpx import HTTPXMock

from harness_python_sdk.base_model import HarnessModel
from harness_python_sdk.client import HarnessClient
from harness_python_sdk.pagination import PaginationStyle


class ItemModel(HarnessModel):
    """Model for paginated items."""

    id: str
    name: str


class TestPaginationOffset:
    """Test offset-based pagination."""

    def test_paginate_offset_single_page(self, httpx_mock: HTTPXMock):
        """Test pagination with single page of results."""
        httpx_mock.add_response(
            json={
                "data": [
                    {"id": "1", "name": "Item1"},
                    {"id": "2", "name": "Item2"},
                ],
                "pageIndex": 0,
                "pageSize": 100,
                "pageItemCount": 2,
                "totalItems": 2,
            }
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                params={"pageSize": 100},
                response_model=ItemModel,
                pagination_style=PaginationStyle.OFFSET,
            )
        )

        assert len(items) == 2
        assert items[0].id == "1"
        assert items[1].id == "2"
        client.close()

    def test_paginate_offset_multiple_pages(self, httpx_mock: HTTPXMock):
        """Test pagination across multiple pages."""
        # Page 0
        httpx_mock.add_response(
            json={
                "data": [{"id": "1", "name": "Item1"}, {"id": "2", "name": "Item2"}],
                "pageIndex": 0,
                "pageSize": 2,
                "pageItemCount": 2,
                "totalItems": 5,
            }
        )
        # Page 1
        httpx_mock.add_response(
            json={
                "data": [{"id": "3", "name": "Item3"}, {"id": "4", "name": "Item4"}],
                "pageIndex": 1,
                "pageSize": 2,
                "pageItemCount": 2,
                "totalItems": 5,
            }
        )
        # Page 2
        httpx_mock.add_response(
            json={
                "data": [{"id": "5", "name": "Item5"}],
                "pageIndex": 2,
                "pageSize": 2,
                "pageItemCount": 1,
                "totalItems": 5,
            }
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                params={"pageSize": 2},
                response_model=ItemModel,
                pagination_style=PaginationStyle.OFFSET,
            )
        )

        assert len(items) == 5
        assert items[0].id == "1"
        assert items[4].id == "5"
        client.close()

    def test_paginate_offset_empty_result(self, httpx_mock: HTTPXMock):
        """Test pagination with empty results."""
        httpx_mock.add_response(
            json={
                "data": [],
                "pageIndex": 0,
                "pageSize": 100,
                "pageItemCount": 0,
                "totalItems": 0,
            }
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                params={"pageSize": 100},
                response_model=ItemModel,
                pagination_style=PaginationStyle.OFFSET,
            )
        )

        assert len(items) == 0
        client.close()


class TestPaginationCursor:
    """Test cursor-based pagination."""

    def test_paginate_cursor_single_page(self, httpx_mock: HTTPXMock):
        """Test cursor pagination with single page of results."""
        httpx_mock.add_response(
            json={
                "data": [
                    {"id": "1", "name": "Item1"},
                    {"id": "2", "name": "Item2"},
                ],
                "pageToken": None,
            }
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                response_model=ItemModel,
                pagination_style=PaginationStyle.CURSOR,
            )
        )

        assert len(items) == 2
        assert items[0].id == "1"
        client.close()

    def test_paginate_cursor_multiple_pages(self, httpx_mock: HTTPXMock):
        """Test cursor pagination across multiple pages."""
        # Page 1
        httpx_mock.add_response(
            json={
                "data": [{"id": "1", "name": "Item1"}, {"id": "2", "name": "Item2"}],
                "pageToken": "token-page-2",
            }
        )
        # Page 2
        httpx_mock.add_response(
            json={
                "data": [{"id": "3", "name": "Item3"}],
                "pageToken": None,
            }
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                response_model=ItemModel,
                pagination_style=PaginationStyle.CURSOR,
            )
        )

        assert len(items) == 3
        assert items[0].id == "1"
        assert items[2].id == "3"
        client.close()

    def test_paginate_cursor_list_response(self, httpx_mock: HTTPXMock):
        """Test cursor pagination when response is a list."""
        httpx_mock.add_response(
            json=[{"id": "1", "name": "Item1"}, {"id": "2", "name": "Item2"}]
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                response_model=ItemModel,
                pagination_style=PaginationStyle.CURSOR,
            )
        )

        assert len(items) == 2
        client.close()


class TestPaginationWithoutModel:
    """Test pagination without response model."""

    def test_paginate_without_model(self, httpx_mock: HTTPXMock):
        """Test pagination without response model returns dicts."""
        httpx_mock.add_response(
            json={
                "data": [
                    {"id": "1", "name": "Item1"},
                    {"id": "2", "name": "Item2"},
                ],
                "pageIndex": 0,
                "pageSize": 100,
                "pageItemCount": 2,
            }
        )

        client = HarnessClient(api_key="key", account_id="acc")
        items = list(
            client._paginate(
                "/test",
                params={"pageSize": 100},
                pagination_style=PaginationStyle.OFFSET,
            )
        )

        assert len(items) == 2
        assert isinstance(items[0], dict)
        assert items[0]["id"] == "1"
        client.close()
