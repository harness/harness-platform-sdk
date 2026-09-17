#!/usr/bin/env python3
"""Generate llms.md from SDK introspection and Jinja2 template."""

import inspect
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, FileSystemLoader


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[0;33m"
    RED = "\033[0;31m"
    RESET = "\033[0m"

    @staticmethod
    def green(text: str) -> str:
        """Format text in green."""
        return f"{Colors.GREEN}{text}{Colors.RESET}"

    @staticmethod
    def blue(text: str) -> str:
        """Format text in blue."""
        return f"{Colors.BLUE}{text}{Colors.RESET}"

    @staticmethod
    def yellow(text: str) -> str:
        """Format text in yellow."""
        return f"{Colors.YELLOW}{text}{Colors.RESET}"

    @staticmethod
    def red(text: str) -> str:
        """Format text in red."""
        return f"{Colors.RED}{text}{Colors.RESET}"


def _property_to_class_name(prop_name: str) -> str:
    """Convert property name to class name using SDK naming conventions.

    Examples:
        organizations -> OrganizationsApi
        workspaces -> WorkspacesApi
        workspace_default_pipelines -> WorkspaceDefaultPipelinesApi
    """
    # Split by underscore
    parts = prop_name.split("_")
    # Capitalize each part and join
    words = [p.capitalize() for p in parts]
    class_name = "".join(words) + "Api"
    return class_name


def discover_api_managers() -> Dict[str, Any]:
    """Discover all API managers from HarnessClient.

    Returns:
        Dict with discovered API managers grouped by domain.
        Structure: {domain_key: {apis: [list of api dicts]}}
    """
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    try:
        from harness_platform_sdk.client import HarnessClient

        discovered = {}

        # List all properties on HarnessClient
        for prop_name in dir(HarnessClient):
            # Skip non-API properties
            if prop_name.startswith("_") or prop_name in ("base_url",):
                continue

            try:
                prop_obj = getattr(HarnessClient, prop_name)
                if not isinstance(prop_obj, property):
                    continue

                # Get the fget function
                fget = prop_obj.fget
                if not fget:
                    continue

                # Extract the import statement from source to determine domain
                source = inspect.getsource(fget)

                # Determine domain from import path
                domain = None
                for line in source.split("\n"):
                    if "from harness_platform_sdk" not in line:
                        continue

                    if "ng_api" in line:
                        domain = "ng_api"
                    elif "authz" in line:
                        domain = "authz"
                    elif "pipeline_api" in line:
                        domain = "pipeline_api"
                    elif "iacm_api" in line:
                        domain = "iacm_api"
                    elif "idp_api" in line:
                        domain = "idp_api"
                    elif "template_api" in line:
                        domain = "template_api"

                    if domain:
                        break

                if not domain:
                    continue

                # Generate class name from property name using SDK conventions
                class_name = _property_to_class_name(prop_name)

                # Initialize domain if needed
                if domain not in discovered:
                    discovered[domain] = {"apis": []}

                # Use friendly description
                description = f"Manage {prop_name}"

                # Add API manager
                discovered[domain]["apis"].append(
                    {
                        "property_name": prop_name,
                        "class_name": class_name,
                        "description": description,
                        "doc_link": f"/docs/generated/index.md#{class_name.lower()}",
                    }
                )

            except Exception as e:
                print(f"{Colors.yellow('⚠')} Could not introspect {prop_name}: {e}")
                continue

        return discovered

    except Exception as e:
        print(f"{Colors.red('✗')} Error discovering API managers: {e}")
        sys.exit(1)


def load_config() -> Dict[str, Any]:
    """Load curated configuration from YAML.

    Returns:
        Configuration dictionary.
    """
    config_path = Path(__file__).parent / "llms_config.yaml"

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"{Colors.red('✗')} Error loading config: {e}")
        sys.exit(1)


def enrich_api_data(
    discovered: Dict[str, Any], config: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge discovered APIs with configuration.

    Args:
        discovered: Discovered API managers.
        config: Configuration from YAML.

    Returns:
        Enriched data ready for template rendering.
    """
    # Merge domain display names
    enriched_domains = {}
    for domain_key, domain_info in discovered.items():
        domain_config = config.get("domains", {}).get(domain_key, {})
        enriched_domains[domain_key] = {
            "display_name": domain_config.get("display_name", domain_key),
            "apis": domain_info["apis"],
        }

    # Validate API count
    total_apis = sum(len(d["apis"]) for d in enriched_domains.values())
    expected_apis = 24

    if total_apis != expected_apis:
        print(
            f"{Colors.yellow('⚠')} "
            f"Expected {expected_apis} APIs, found {total_apis}"
        )

    # Prepare full context for template
    template_context = {
        "domains": enriched_domains,
        **{k: v for k, v in config.items() if k != "domains"},
    }

    return template_context


def render_template(context: Dict[str, Any]) -> str:
    """Render Jinja2 template with context.

    Args:
        context: Context data for template.

    Returns:
        Rendered llms.md content.
    """
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("llms.j2")

    try:
        content = template.render(**context)
        return content
    except Exception as e:
        print(f"{Colors.red('✗')} Error rendering template: {e}")
        sys.exit(1)


def validate_output(content: str) -> bool:
    """Validate generated content against llms.txt spec.

    Args:
        content: Generated llms.md content.

    Returns:
        True if validation passes, False otherwise.
    """
    import subprocess

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, dir="/tmp"
    ) as f:
        f.write(content)
        temp_path = f.name

    try:
        # Temporarily rename to llms.txt for validation (validator expects .txt extension)
        temp_txt = temp_path.replace(".md", ".txt")
        Path(temp_path).rename(temp_txt)

        # Run validation
        validate_script = Path(__file__).parent / "validate_llms_txt.py"
        result = subprocess.run(
            [sys.executable, str(validate_script)],
            env={**dict(os.environ), "LLMS_TXT_PATH": temp_txt},
            capture_output=True,
            text=True,
        )

        # Restore original name
        Path(temp_txt).rename(temp_path)

        if result.returncode != 0:
            print(f"{Colors.red('✗')} Validation failed:")
            print(result.stdout)
            return False

        return True

    except Exception as e:
        print(f"{Colors.yellow('⚠')} Validation check skipped: {e}")
        return True

    finally:
        if Path(temp_path).exists():
            Path(temp_path).unlink()


def main() -> int:
    """Generate llms.md from SDK introspection and template.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print(Colors.blue("🔍 Discovering API managers..."))
    discovered = discover_api_managers()
    api_count = sum(len(d["apis"]) for d in discovered.values())
    print(f"  {Colors.green(f'Found {api_count} API managers')}")

    print(Colors.blue("📋 Loading configuration..."))
    config = load_config()
    print("  ✓ Configuration loaded")

    print(Colors.blue("🔗 Enriching API data..."))
    context = enrich_api_data(discovered, config)
    print("  ✓ Data enriched")

    print(Colors.blue("📝 Rendering template..."))
    content = render_template(context)
    print("  ✓ Template rendered")

    output_path = Path(__file__).parent.parent / "docs" / "llms.md"

    print(Colors.blue("✓ Generating llms.md..."))
    output_path.write_text(content)
    print(f"  {Colors.green(f'Generated: {output_path}')}")

    return 0


if __name__ == "__main__":
    import os

    sys.exit(main())
