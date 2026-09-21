# Copyright (c) 2025 Harness Solution Factory. All Rights Reserved.
"""Test docstrings exist and are properly formatted across the SDK."""

import ast
import inspect
import re
from pathlib import Path

import pytest

# Get the source module path
MODULE_PATH = Path(__file__).parent.parent / "src" / "harness_platform_sdk"


def get_public_members(module_path: Path):
    """Get all public functions, classes, and methods from a module."""
    with open(module_path) as f:
        tree = ast.parse(f.read())

    members = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Skip private members (starting with _)
            if not node.name.startswith("_"):
                members.append((node.name, node))
            elif node.name == "__init__":  # Include __init__ methods
                members.append((node.name, node))

    return members


def has_docstring(node: ast.AST) -> bool:
    """Check if AST node has a docstring."""
    return (
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and ast.get_docstring(node) is not None
    )


def docstring_ends_with_period(docstring: str) -> bool:
    """Check if docstring ends with proper punctuation."""
    if not docstring:
        return False
    first_line = docstring.split("\n")[0].strip()
    return first_line and first_line[-1] in ".!?"


def is_valid_docstring(docstring: str) -> bool:
    """Validate docstring format."""
    if not docstring:
        return False
    # Check for minimum length
    first_line = docstring.split("\n")[0].strip()
    if len(first_line) < 5:
        return False
    # Check for ending punctuation
    return docstring_ends_with_period(docstring)


@pytest.mark.parametrize(
    "py_file",
    sorted(
        MODULE_PATH.glob("*.py"),
        key=lambda x: x.name,
    ),
)
class TestModuleDocstrings:
    """Test that all modules have valid docstrings."""

    def test_module_has_docstring(self, py_file: Path):
        """Verify module has a docstring."""
        with open(py_file) as f:
            content = f.read()
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)

        assert docstring is not None, f"{py_file.name} is missing module docstring"

    def test_module_docstring_ends_with_period(self, py_file: Path):
        """Verify module docstring ends with punctuation."""
        with open(py_file) as f:
            content = f.read()
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)

        if docstring:
            first_line = docstring.split("\n")[0].strip()
            assert (
                first_line[-1] in ".!?"
            ), f"{py_file.name}: module docstring missing ending punctuation"

    def test_public_functions_have_docstrings(self, py_file: Path):
        """Verify all public functions have docstrings."""
        if py_file.name == "__init__.py":
            pytest.skip("Skipping __init__.py")

        members = get_public_members(py_file)
        for name, node in members:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                assert has_docstring(node), f"{py_file.name}::{name} is missing docstring"

    def test_public_classes_have_docstrings(self, py_file: Path):
        """Verify all public classes have docstrings."""
        if py_file.name == "__init__.py":
            pytest.skip("Skipping __init__.py")

        members = get_public_members(py_file)
        for name, node in members:
            if isinstance(node, ast.ClassDef):
                assert has_docstring(node), f"{py_file.name}::{name} is missing docstring"

    def test_init_methods_have_docstrings(self, py_file: Path):
        """Verify all __init__ methods have docstrings."""
        if py_file.name == "__init__.py":
            pytest.skip("Skipping __init__.py")

        members = get_public_members(py_file)
        for name, node in members:
            if name == "__init__":
                assert has_docstring(node), f"{py_file.name}::{name} is missing docstring"

    def test_function_docstrings_end_with_period(self, py_file: Path):
        """Verify function docstrings end with punctuation."""
        if py_file.name == "__init__.py":
            pytest.skip("Skipping __init__.py")

        members = get_public_members(py_file)
        for name, node in members:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    first_line = docstring.split("\n")[0].strip()
                    assert (
                        first_line[-1] in ".!?"
                    ), f"{py_file.name}::{name}: docstring missing ending punctuation"

    def test_class_docstrings_end_with_period(self, py_file: Path):
        """Verify class docstrings end with punctuation."""
        if py_file.name == "__init__.py":
            pytest.skip("Skipping __init__.py")

        members = get_public_members(py_file)
        for name, node in members:
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    first_line = docstring.split("\n")[0].strip()
                    assert (
                        first_line[-1] in ".!?"
                    ), f"{py_file.name}::{name}: docstring missing ending punctuation"
