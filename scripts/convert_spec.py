# GENERATED — do not edit. Run mise run regenerate to update.
#!/usr/bin/env python3
"""
Convert normalized OpenAPI YAML to JSON.

Reads: openapi/harness-openapi-normalized.yaml
Writes: openapi/harness-openapi-normalized.json
"""

import json
import sys
from pathlib import Path

import yaml


INPUT_YAML = Path(__file__).parent.parent / "openapi" / "harness-openapi-normalized.yaml"
OUTPUT_JSON = Path(__file__).parent.parent / "openapi" / "harness-openapi-normalized.json"


def main():
    """Convert YAML to JSON."""
    print(f"Reading {INPUT_YAML}...")
    with open(INPUT_YAML, "r") as f:
        spec = yaml.safe_load(f)

    print(f"Writing {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, "w") as f:
        json.dump(spec, f, indent=2)

    print(f"✓ Conversion complete: {OUTPUT_JSON.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
