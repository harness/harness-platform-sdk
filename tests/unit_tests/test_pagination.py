"""Unit tests for pagination support."""

from harness_platform_sdk.pagination import PaginationStyle


class TestPaginationStyle:
    """Test PaginationStyle enum."""

    def test_offset_enum_value(self):
        """Test that OFFSET enum has correct string value."""
        assert PaginationStyle.OFFSET == "offset"
        assert PaginationStyle.OFFSET.value == "offset"

    def test_cursor_enum_value(self):
        """Test that CURSOR enum has correct string value."""
        assert PaginationStyle.CURSOR == "cursor"
        assert PaginationStyle.CURSOR.value == "cursor"

    def test_pagination_style_from_string(self):
        """Test creating PaginationStyle from string."""
        assert PaginationStyle("offset") == PaginationStyle.OFFSET
        assert PaginationStyle("cursor") == PaginationStyle.CURSOR

    def test_pagination_style_comparison(self):
        """Test PaginationStyle enum comparison."""
        assert PaginationStyle.OFFSET == PaginationStyle.OFFSET
        assert PaginationStyle.CURSOR == PaginationStyle.CURSOR
        assert PaginationStyle.OFFSET != PaginationStyle.CURSOR

    def test_pagination_style_is_string_enum(self):
        """Test that PaginationStyle is a string-based enum."""
        # Should be usable as string
        style = PaginationStyle.OFFSET
        assert isinstance(style, str)
        assert style == "offset"
        assert style.value == "offset"

    def test_pagination_style_valid_values(self):
        """Test all valid PaginationStyle values."""
        valid_values = ["offset", "cursor"]
        for value in valid_values:
            style = PaginationStyle(value)
            assert style is not None
            assert style.value == value

    def test_pagination_style_invalid_value(self):
        """Test that invalid PaginationStyle value raises."""
        try:
            PaginationStyle("invalid")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_pagination_style_in_condition(self):
        """Test PaginationStyle in conditional checks."""
        style = PaginationStyle.OFFSET
        if style == PaginationStyle.OFFSET:
            result = "offset_used"
        elif style == PaginationStyle.CURSOR:
            result = "cursor_used"
        else:
            result = "unknown"
        assert result == "offset_used"

    def test_pagination_style_all_members(self):
        """Test all members of PaginationStyle."""
        members = list(PaginationStyle)
        assert len(members) == 2
        assert PaginationStyle.OFFSET in members
        assert PaginationStyle.CURSOR in members
