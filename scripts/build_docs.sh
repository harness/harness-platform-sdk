#!/bin/bash
# Build markdown documentation from docstrings

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building markdown documentation...${NC}"

# Create output directory
OUTPUT_DIR="docs/generated"
mkdir -p "$OUTPUT_DIR"

# Use Python script to generate markdown from docstrings
python3 << 'PYTHON_EOF'
import json
import os
from pathlib import Path
from typing import Any, Dict

def get_module_info(module_path: str) -> Dict[str, Any]:
    """Extract module docstring and basic info."""
    try:
        with open(module_path, 'r') as f:
            content = f.read()
            # Simple extraction of module docstring
            if content.strip().startswith('"""'):
                end = content.find('"""', 3)
                if end != -1:
                    docstring = content[3:end].strip()
                    return {
                        'path': module_path,
                        'docstring': docstring
                    }
    except Exception as e:
        print(f"Error processing {module_path}: {e}")
    return None

# Scan harness_platform_sdk modules
sdk_dir = Path("src/harness_platform_sdk")
output_dir = Path("docs/generated")
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
        index_content += f"- `{module_name}` — {info['docstring'].split(chr(10))[0]}\n"

# Write index
index_file = output_dir / "index.md"
index_file.write_text(index_content)

print(f"✅ Generated index: {index_file}")
print(f"📁 Output directory: {output_dir}/")

PYTHON_EOF

echo -e "${GREEN}✅ Documentation skeleton generated${NC}"
echo ""
echo -e "${BLUE}Note: For full markdown API docs, run:${NC}"
echo "  python3 -m pdoc --markdown -o docs/generated harness_platform_sdk"
echo ""
echo -e "${GREEN}✅ Markdown build setup complete${NC}"
