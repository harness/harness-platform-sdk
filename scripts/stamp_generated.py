# GENERATED — do not edit. Run mise run regenerate to update.
#!/usr/bin/env python3
"""
Post-process generated models: add GENERATED header and rewrite BaseModel -> HarnessModel.

Processes all .py files in models/staging/ and domain directories.
"""

import re
import sys
from pathlib import Path


GENERATED_HEADER = "# GENERATED — do not edit. Run mise run regenerate to update."
HARNESS_MODEL_IMPORT = "from harness_python_sdk.base_model import HarnessModel"

MODELS_ROOT = Path(__file__).parent.parent

def process_file(file_path: Path) -> int:
    """Process a single Python file. Return 1 if modified, 0 otherwise."""
    with open(file_path, "r") as f:
        content = f.read()

    original_content = content
    lines = content.split("\n")

    # Check if GENERATED header already present
    has_header = len(lines) > 0 and GENERATED_HEADER in lines[0]

    if not has_header:
        # Add header as first line
        lines.insert(0, GENERATED_HEADER)

    # Rejoin and process inheritance rewrite
    content = "\n".join(lines)

    # Replace class X(HarnessModel): with class X(HarnessModel):
    content = re.sub(
        r"\bclass\s+(\w+)\(BaseModel\)",
        r"class \1(HarnessModel)",
        content,
    )

    # Ensure HarnessModel import is present if we have any classes inheriting from it
    if "HarnessModel" in content:
        if HARNESS_MODEL_IMPORT not in content:
            # Add import after other imports
            import_match = re.search(r"(from pydantic import.*?\n)", content)
            if import_match:
                # Add after pydantic imports
                insert_pos = import_match.end()
                content = content[:insert_pos] + HARNESS_MODEL_IMPORT + "\n" + content[insert_pos:]
            else:
                # No pydantic import, add at top after GENERATED header
                lines = content.split("\n")
                # Find first non-comment/empty line after header
                insert_idx = 1  # After GENERATED header
                while insert_idx < len(lines) and (
                    lines[insert_idx].startswith("#") or not lines[insert_idx].strip()
                ):
                    insert_idx += 1
                lines.insert(insert_idx, HARNESS_MODEL_IMPORT)
                content = "\n".join(lines)

    # Only write if changed
    if content != original_content:
        with open(file_path, "w") as f:
            f.write(content)
        return 1
    return 0


def main():
    """Process all generated Python files."""
    print(f"Processing generated files in {MODELS_ROOT}...")

    # Find all .py files in staging and domain directories
    py_files = []
    staging_dir = MODELS_ROOT / "staging"
    if staging_dir.exists():
        py_files.extend(staging_dir.glob("*.py"))

    # Also process any already-sorted domain directories
    for domain_dir in MODELS_ROOT.glob("*"):
        if domain_dir.is_dir() and domain_dir.name not in ("staging", "_spike"):
            py_files.extend(domain_dir.glob("*.py"))

    if not py_files:
        print("No Python files found.")
        return 0

    print(f"Found {len(py_files)} Python files.")
    modified = 0

    for file_path in sorted(py_files):
        # Skip __init__.py files - these should remain as simple markers
        if file_path.name == "__init__.py":
            continue
        if process_file(file_path):
            modified += 1
            print(f"  ✓ {file_path.relative_to(MODELS_ROOT)}")

    print(f"\nModified {modified} files.")

    # Ensure all domain directories have simple marker __init__.py files
    all_domains = ["staging", "_spike", "pipelines", "connectors", "secrets", "infrastructure",
                   "access_control", "environments", "projects", "organizations", "cost",
                   "governance", "cloud", "audit", "gitops", "chaos", "misc"]
    for domain in all_domains:
        domain_dir = MODELS_ROOT / domain
        if domain_dir.is_dir():
            init_file = domain_dir / "__init__.py"
            init_file.write_text("# This file intentionally left mostly empty\n")

    print("✓ Reset all __init__.py files to simple markers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
