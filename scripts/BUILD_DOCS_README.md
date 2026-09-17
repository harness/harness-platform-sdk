# Build Docs Script

This directory contains documentation build tools for the Harness Platform SDK.

## `build_docs.py`

Pure Python implementation of the documentation builder (replaces `build_docs.sh`).

### Features

- ✅ Generates markdown documentation index from SDK docstrings
- ✅ Color-coded terminal output
- ✅ Proper error handling and exit codes
- ✅ Type hints for code quality
- ✅ Self-contained, no external shell dependencies

### Usage

```bash
python3 scripts/build_docs.py
```

Or make it executable and run directly:

```bash
chmod +x scripts/build_docs.py
./scripts/build_docs.py
```

### Output

Generates: `docs/generated/index.md`

This index file:
- Lists all modules in the SDK
- Extracts first-line docstrings for each module
- Provides a quick reference for API structure

### Requirements

- Python 3.7+
- No external dependencies (uses stdlib only)

### Exit Codes

- `0` — Success
- `1` — Error (SDK directory not found or other failure)

### Integration

Can be called from:
- CI/CD pipelines
- Build scripts
- Automated documentation generation workflows

### Example

```python
from pathlib import Path
from scripts.build_docs import generate_markdown_docs

sdk_dir = Path("src/harness_platform_sdk")
output_dir = Path("docs/generated")
generate_markdown_docs(sdk_dir, output_dir)
```

### Next Steps

For full markdown API documentation with method signatures, use:

```bash
python3 -m pdoc --markdown -o docs/generated harness_platform_sdk
```

This uses pdoc3 to generate complete markdown for all symbols in the SDK.

