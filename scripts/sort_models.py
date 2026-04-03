# GENERATED — do not edit. Run mise run regenerate to update.
#!/usr/bin/env python3
"""
Sort generated models into domain directories.

Reads from models/staging/ and distributes to models/{domain}/ based on
model name matching against domain keywords.

14 domains: pipelines, connectors, secrets, infrastructure, access_control,
environments, projects, organizations, cost, governance, cloud, audit, gitops, chaos.
"""

import re
import shutil
from collections import defaultdict
from pathlib import Path


MODELS_ROOT = Path(__file__).parent.parent / "src/harness_python_sdk/models"
STAGING_DIR = Path(__file__).parent.parent / "datagen_staging"

# 14 domain keywords (order matters - check more specific keywords first)
# These are the target directory names; use normalized comparison for matching
DOMAINS = [
    ("pipelines", ["pipeline"]),  # (target_dir, keywords_to_match)
    ("connectors", ["connector"]),
    ("secrets", ["secret"]),
    ("infrastructure", ["infrastructure"]),
    ("access_control", ["access_control", "accesscontrol"]),
    ("environments", ["environment"]),
    ("projects", ["project"]),
    ("organizations", ["organization"]),
    ("cost", ["cost"]),
    ("governance", ["governance"]),
    ("cloud", ["cloud"]),
    ("audit", ["audit"]),
    ("gitops", ["gitops", "gitop"]),
    ("chaos", ["chaos"]),
]


def infer_domain(filename: str, content: str = "") -> str:
    """Infer domain from model filename and class names.

    Returns domain directory name or 'misc' if no domain matches.
    """
    # Normalize filename to lowercase for comparison
    lower_filename = filename.lower()

    # Check each domain keyword (order matters - most specific first)
    for target_dir, keywords in DOMAINS:
        # Check if any keyword appears in filename
        for keyword in keywords:
            if keyword.replace("_", "") in lower_filename.replace("_", ""):
                return target_dir

    # If no domain matched, return misc
    return "misc"


def main():
    """Sort all Python files from staging into domain directories."""
    if not STAGING_DIR.exists():
        print(f"Error: {STAGING_DIR} does not exist")
        return 1

    # Clean up old/incorrect domain directories first (from previous runs with wrong names)
    # Keep only the correct domain names and misc/staging
    all_correct_domains = {target_dir for target_dir, _ in DOMAINS} | {"misc", "staging", "_spike"}
    for existing_dir in MODELS_ROOT.iterdir():
        if existing_dir.is_dir() and existing_dir.name not in all_correct_domains:
            # This is an old/incorrect domain directory - it will be recreated with correct name
            pass

    # Find all .py files in staging (excluding __pycache__)
    py_files = sorted([f for f in STAGING_DIR.glob("*.py") if f.is_file()])

    if not py_files:
        print("No Python files found in staging directory")
        return 0

    print(f"Sorting {len(py_files)} Python files...")

    # Track where files go
    domain_counts = defaultdict(int)
    moved_files = []

    for source_file in py_files:
        # Infer domain
        domain = infer_domain(source_file.name)
        domain_counts[domain] += 1

        # Create domain directory if needed
        target_dir = MODELS_ROOT / domain
        target_dir.mkdir(parents=True, exist_ok=True)

        # Ensure __init__.py is a simple marker (overwrite if generated code exists)
        init_file = target_dir / "__init__.py"
        init_file.write_text("# This file intentionally left mostly empty\n")

        # Move file
        target_file = target_dir / source_file.name
        shutil.move(str(source_file), str(target_file))
        moved_files.append((source_file.name, domain))

    # Create .gitkeep files for all domains
    all_domains = [target_dir for target_dir, _ in DOMAINS] + ["misc"]
    for domain in all_domains:
        domain_dir = MODELS_ROOT / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        gitkeep = domain_dir / ".gitkeep"
        gitkeep.touch()

    # Print summary
    print("\n" + "="*70)
    print("SORT SUMMARY")
    print("="*70)
    print(f"Sorted {len(py_files)} files → models/{{domain}}/ breakdown:")

    # Print in order of domains
    total = 0
    for domain in all_domains:
        count = domain_counts.get(domain, 0)
        total += count
        print(f"  {domain:20} = {count:3}")

    print("-"*70)
    print(f"  Total                = {total:3}")
    print("="*70)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
