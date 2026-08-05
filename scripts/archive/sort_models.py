# GENERATED — do not edit. Run mise run regenerate to update.
#!/usr/bin/env python3
"""
Sort generated models into domain directories.

Reads from models/staging/ and distributes to models/{domain}/ based on
model name matching against domain keywords.

14 domains: pipelines, connectors, secrets, infrastructure, access_control,
environments, projects, organizations, cost, governance, cloud, audit, gitops, chaos.
"""

import ast
import re
import shutil
from collections import defaultdict
from pathlib import Path


MODELS_ROOT = Path(__file__).parent.parent / "src/harness_python_sdk/models"
STAGING_DIR = Path(__file__).parent.parent / "datagen_staging"

# Prefix-to-domain mapping from dotted schema renames
# Used as first-pass lookup before keyword scan (longest-first matching)
DOTTED_PREFIX_DOMAIN = {
    # Chaos Engineering
    "action":                    "chaos",
    "actions":                   "chaos",
    "applicationchaostarget":    "chaos",
    "bulkaction":                "chaos",
    "chaosactiontemplate":       "chaos",
    "chaoscomponent":            "chaos",
    "chaoscomponents":           "chaos",
    "chaosexperiment":           "chaos",
    "chaosexperimentpipeline":   "chaos",
    "chaosexperimenttemplate":   "chaos",
    "chaosfault":                "chaos",
    "chaosfaulttemplate":        "chaos",
    "chaosguardconditions":      "chaos",
    "chaosguardrules":           "chaos",
    "chaoshub":                  "chaos",
    "chaoshubresources":         "chaos",
    "chaoshubv2":                "chaos",
    "chaosprobetemplate":        "chaos",
    "chaosresourcenotes":        "chaos",
    "chaosserviceusage":         "chaos",
    "experiment":                "chaos",
    "experimenttemplate":        "chaos",
    "fault":                     "chaos",
    "faulttemplate":             "chaos",
    "handlers":                  "chaos",
    "hcesdk":                    "chaos",
    "image_registry":            "chaos",
    "infra":                     "chaos",
    "infra_v2":                  "chaos",
    "k8sinfra":                  "chaos",
    "kubernetes_infra":          "chaos",
    "model":                     "chaos",
    "networkmap":                "chaos",
    "probe":                     "chaos",
    "recommendation":            "chaos",
    "recommendations":           "chaos",
    "risks":                     "chaos",
    "targetnetworkmap":          "chaos",
    "targetservice":             "chaos",
    "types":                     "chaos",
    # Pipelines
    "execution":                 "pipelines",
    "inputset":                  "pipelines",
    "inputsets":                 "pipelines",
    "pipelineonboarding":        "pipelines",
    "pipelines":                 "pipelines",
    # GitOps
    "api":                       "gitops",
    "appprojects":               "gitops",
    "applications":              "gitops",
    "common":                    "gitops",
    "common_types":              "gitops",
    "database":                  "gitops",
    "intstr":                    "gitops",
    "k8s_io_api_core_v1":        "gitops",
    "k8s_io_apimachinery_pkg_apis_meta_v1": "gitops",
    "mongodb":                   "gitops",
    "openapi":                   "gitops",
    "repositories":              "gitops",
    "resource":                  "gitops",
    "servicev1":                 "gitops",
    "shared":                    "gitops",
    "v1":                        "gitops",
    "v1alpha1":                  "gitops",
    "v2_onboarding":             "gitops",
    "v3":                        "gitops",
    # Governance
    "security_governance":       "governance",
    # Cost
    "parser":                    "cost",
}

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


def _domain_from_prefix(stem: str) -> str | None:
    """Return domain for a file stem based on its renamed dotted prefix.

    Iterates DOTTED_PREFIX_DOMAIN longest-key-first to prevent short keys
    (e.g. 'infra') matching before longer ones ('infra_v2').
    Returns None if no prefix matches.
    """
    for prefix in sorted(DOTTED_PREFIX_DOMAIN, key=len, reverse=True):
        if stem == prefix or stem.startswith(prefix + "_"):
            return DOTTED_PREFIX_DOMAIN[prefix]
    return None


def infer_domain(filename: str, content: str = "") -> tuple[str, bool]:
    """Infer domain from model filename and class names.

    Returns tuple of (domain_directory_name, matched_via_prefix_map).
    'matched_via_prefix_map' is True if the file was sorted by the prefix-map lookup.
    """
    # Extract stem (filename without .py extension)
    stem = filename[:-3] if filename.endswith(".py") else filename

    # First pass: check dotted-prefix mapping (longest-first)
    domain = _domain_from_prefix(stem)
    if domain is not None:
        return domain, True

    # Second pass: check keyword matching (existing logic)
    lower_filename = filename.lower()
    for target_dir, keywords in DOMAINS:
        # Check if any keyword appears in filename
        for keyword in keywords:
            if keyword.replace("_", "") in lower_filename.replace("_", ""):
                return target_dir, False

    # If no domain matched, return misc
    return "misc", False


def _extract_public_classes(file_path: Path) -> list[str]:
    """Extract public class names from a Python file using AST.

    Returns sorted list of class names that don't start with underscore.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        public_classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                public_classes.append(node.name)

        return sorted(public_classes)  # Sort for determinism
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Failed to parse {file_path}: {e}")
        return []


def _generate_domain_init(domain_dir: Path, domain_name: str, models_root: Path = None) -> tuple[int, int]:
    """Generate populated __init__.py for a domain directory.

    Returns tuple of (num_files_processed, num_classes_exported).
    """
    if models_root is None:
        models_root = domain_dir.parent

    # Find all .py files, exclude __init__.py, sort for determinism
    py_files = sorted([
        f for f in domain_dir.glob("*.py")
        if f.is_file() and f.name != "__init__.py"
    ])

    if not py_files:
        # Empty domain - create marker
        init_file = domain_dir / "__init__.py"
        init_file.write_text(
            "# GENERATED — do not edit. Run mise run regenerate to update.\n"
            f"# Auto-generated exports for harness_python_sdk.models.{domain_name}\n"
            "# (empty domain)\n"
        )
        return 0, 0

    # Extract classes from each file and collect all module names
    exports = []  # List of (module_name, [class_names])
    module_names = []  # All module names for re-importing
    for py_file in py_files:
        module_name = py_file.stem
        module_names.append(module_name)
        classes = _extract_public_classes(py_file)
        if classes:
            exports.append((module_name, classes))

    # Generate __init__.py that re-exports all public classes
    # Per spec: "one `from .{module_stem} import {ClassName1}, {ClassName2}` line per source file"
    import_lines = []

    # Import all classes for re-export from this domain
    for module_name, classes in exports:
        class_list = ", ".join(classes)
        import_lines.append(f"from .{module_name} import {class_list}")

    # Write __init__.py
    init_file = domain_dir / "__init__.py"
    content = (
        "# GENERATED — do not edit. Run mise run regenerate to update.\n"
        f"# Auto-generated exports for harness_python_sdk.models.{domain_name}\n"
        "\n"
        + "\n".join(import_lines)
        + "\n"
    )
    init_file.write_text(content)

    total_classes = sum(len(classes) for _, classes in exports)
    return len(py_files), total_classes


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
    prefix_map_hits = 0
    moved_files = []

    for source_file in py_files:
        # Infer domain
        domain, matched_via_prefix = infer_domain(source_file.name)
        domain_counts[domain] += 1
        if matched_via_prefix:
            prefix_map_hits += 1

        # Create domain directory if needed
        target_dir = MODELS_ROOT / domain
        target_dir.mkdir(parents=True, exist_ok=True)

        # Move file
        target_file = target_dir / source_file.name
        shutil.move(str(source_file), str(target_file))
        moved_files.append((source_file.name, domain))

    # Generate __init__.py files for all domains with files
    print("\nGenerating domain __init__.py files...")
    total_domains = 0
    total_exports = 0
    export_stats = []  # For summary

    all_domains_list = [target_dir for target_dir, _ in DOMAINS] + ["misc"]
    for domain in all_domains_list:
        domain_dir = MODELS_ROOT / domain
        if domain_dir.exists() and any(domain_dir.glob("*.py")):
            num_files, num_exports = _generate_domain_init(domain_dir, domain, MODELS_ROOT)
            if num_exports > 0:
                export_stats.append((domain, num_files, num_exports))
                total_domains += 1
                total_exports += num_exports
                print(f"  ✓ {domain}: {num_exports} exports from {num_files} files")

    print(f"\nGenerated {total_domains} domain packages with {total_exports} total exports")

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
    print(f"(prefix-map lookup active — {prefix_map_hits} files resolved via dotted-schema rename table)")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
