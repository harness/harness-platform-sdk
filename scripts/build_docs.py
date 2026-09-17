#!/usr/bin/env python3
"""Build markdown documentation from SDK docstrings."""

import sys
from pathlib import Path
from typing import Any, Dict, Optional


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    RESET = "\033[0m"

    @staticmethod
    def green(text: str) -> str:
        """Format text in green."""
        return f"{Colors.GREEN}{text}{Colors.RESET}"

    @staticmethod
    def blue(text: str) -> str:
        """Format text in blue."""
        return f"{Colors.BLUE}{text}{Colors.RESET}"


def get_module_info(module_path: str) -> Optional[Dict[str, Any]]:
    """Extract module docstring and basic info.

    Args:
        module_path: Path to Python module file.

    Returns:
        Dictionary with path and docstring, or None if extraction fails.
    """
    try:
        with open(module_path, "r") as f:
            content = f.read()
            # Simple extraction of module docstring
            if content.strip().startswith('"""'):
                end = content.find('"""', 3)
                if end != -1:
                    docstring = content[3:end].strip()
                    return {"path": module_path, "docstring": docstring}
    except Exception as e:
        print(f"Error processing {module_path}: {e}")
    return None


def generate_markdown_docs(sdk_dir: Path, output_dir: Path) -> None:
    """Generate markdown documentation from SDK docstrings.

    Args:
        sdk_dir: Path to SDK source directory.
        output_dir: Path to output directory for generated docs.
    """
    print(Colors.blue("Building markdown documentation..."))

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating markdown from docstrings...")

    # Create index file
    index_content = """# Harness Platform SDK API Reference

This documentation is auto-generated from the SDK's docstrings.

## Modules

"""

    # Find all Python modules
    for py_file in sorted(sdk_dir.rglob("*.py")):
        if "__pycache__" in str(py_file):
            continue

        relative = py_file.relative_to(sdk_dir)
        module_name = str(relative.with_suffix("")).replace("/", ".")

        info = get_module_info(str(py_file))
        if info:
            # Get first line of docstring
            first_line = info["docstring"].split("\n")[0]
            index_content += f"- `{module_name}` — {first_line}\n"

    # Write index
    index_file = output_dir / "index.md"
    index_file.write_text(index_content)

    print(f"✅ Generated index: {index_file}")
    print(f"📁 Output directory: {output_dir}/")

    print(Colors.green("✅ Documentation skeleton generated"))
    print()
    print(Colors.blue("Note: For full markdown API docs, run:"))
    print("  python3 -m pdoc -o docs/generated harness_platform_sdk")
    print()
    print(Colors.green("✅ Markdown build setup complete"))


def main() -> int:
    """Main entry point for documentation builder.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    try:
        # Define directories
        sdk_dir = Path("src/harness_platform_sdk")
        output_dir = Path("docs/generated")

        # Verify SDK directory exists
        if not sdk_dir.exists():
            print(f"Error: SDK directory not found: {sdk_dir}", file=sys.stderr)
            return 1

        # Generate documentation
        generate_markdown_docs(sdk_dir, output_dir)
        return 0

    except Exception as e:
        print(f"Error building documentation: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
