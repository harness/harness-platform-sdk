#!/usr/bin/env python3
"""Retrieve IACM workspace details and export as environment variables.

This script connects to a remote Harness account to retrieve detailed
information about a specific IACM workspace and exports its configuration
as environment variables for downstream consumption (e.g., Terraform).

Usage:
    python Return_IACM_Workspace_Details.py --project myproject --workspace myworkspace
    eval "$(python Return_IACM_Workspace_Details.py --project myproject --workspace myworkspace)"
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import yaml

from harness_platform_sdk import HarnessClient, HarnessConfig
from harness_platform_sdk.scope import Scope

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def filter_variables_by_type(variables: dict, target_type: str) -> dict:
    """Filter variables by value_type and extract key-value pairs.

    Args:
        variables: Dictionary where each value is an object with 'key', 'value', 'value_type' fields.
        target_type: The value_type to filter for (e.g., 'string', 'secret').

    Returns:
        dict: Filtered dictionary with {key: value} for matching entries.
    """
    if not variables or not isinstance(variables, dict):
        return {}

    result = {}
    for key, var_obj in variables.items():
        if not isinstance(var_obj, dict):
            logger.warning(f"Variable '{key}' is not a dict, skipping")
            continue

        value_type = var_obj.get("value_type", "string")
        if not value_type:
            logger.warning(f"Variable '{key}' has empty value_type, treating as 'string'")
            value_type = "string"

        if value_type == target_type:
            value = var_obj.get("value")
            result[key] = value

    return result


def resolve_config_from_sources() -> HarnessConfig:
    """Load Harness configuration from multiple sources with precedence.

    Precedence (highest to lowest):
    1. Environment variables (HARNESS_URI, HARNESS_ACCOUNT_ID, HARNESS_API_KEY)
    2. .harness.yaml file (if present)

    Returns:
        HarnessConfig: Configuration object with API credentials.

    Raises:
        ValueError: If no valid configuration source is found.
    """
    config_data = {}
    sources_tried = []

    # Try loading from .harness.yaml first (lowest priority)
    config_file_path = Path(__file__).resolve().parent.parent / ".harness.yaml"
    if config_file_path.exists():
        logger.debug(f"Found .harness.yaml at {config_file_path}")
        try:
            with open(config_file_path, "r") as file:
                file_data = yaml.safe_load(file)
            if file_data:
                config_data.update(file_data)
                sources_tried.append("file")
                logger.debug(f"Loaded config from .harness.yaml")
        except Exception as e:
            logger.warning(f"Failed to load .harness.yaml: {e}")

    # Override with environment variables (higher priority)
    env_config = {}
    env_var_mappings = {
        "HARNESS_URI": "base_url",
        "HARNESS_ACCOUNT_ID": "account_id",
        "HARNESS_API_KEY": "api_key",
    }

    for env_var, config_key in env_var_mappings.items():
        value = os.environ.get(env_var, "").strip()
        if value:
            env_config[config_key] = value

    if env_config:
        config_data.update(env_config)
        sources_tried.append("environment")
        logger.debug(f"Loaded config from environment variables: {', '.join(env_config.keys())}")

    if not config_data:
        sources_list = " or ".join(sources_tried) if sources_tried else "any"
        raise ValueError(
            f"No Harness configuration found. Provide via .harness.yaml or set "
            f"HARNESS_URI, HARNESS_ACCOUNT_ID, HARNESS_API_KEY environment variables."
        )

    # Validate required fields
    required_fields = {"base_url", "account_id", "api_key"}
    missing_fields = required_fields - set(config_data.keys())
    if missing_fields:
        raise ValueError(
            f"Missing required configuration fields: {', '.join(missing_fields)}. "
            f"Provide via .harness.yaml or environment variables (HARNESS_URI, HARNESS_ACCOUNT_ID, HARNESS_API_KEY)."
        )

    return HarnessConfig(**config_data)


def resolve_parameters(args) -> tuple[str, str, str, bool]:
    """Resolve script parameters from CLI args and environment variables.

    Precedence (highest to lowest):
    1. CLI arguments
    2. Environment variables
    3. Defaults (only for org)

    Args:
        args: Parsed command-line arguments from argparse.

    Returns:
        tuple: (project, workspace, org, debug_mode)

    Raises:
        ValueError: If required parameters are missing.
    """
    # Resolve project
    project = args.project or os.environ.get("HARNESS_PROJECT_ID", "").strip()
    if not project:
        raise ValueError(
            "Project ID is required. Provide via --project argument or HARNESS_PROJECT_ID environment variable."
        )

    # Resolve workspace
    workspace = args.workspace or os.environ.get("HARNESS_WORKSPACE_ID", "").strip()
    if not workspace:
        raise ValueError(
            "Workspace ID is required. Provide via --workspace argument or HARNESS_WORKSPACE_ID environment variable."
        )

    # Resolve org (with default)
    org = args.org
    if not org or org == "default":
        env_org = os.environ.get("HARNESS_ORG_ID", "").strip()
        if env_org:
            org = env_org
        else:
            org = "default"

    # Resolve debug mode (accepts: true/True/TRUE/1)
    debug = args.debug
    if not debug:
        debug_env = os.environ.get("DEBUG_MODE", "").strip()
        debug = debug_env.lower() in ("true", "1")

    logger.debug(f"Resolved parameters: project={project}, workspace={workspace}, org={org}, debug={debug}")

    return project, workspace, org, debug


def get_workspace_details(
    client: HarnessClient,
    account_id: str,
    org: str,
    project: str,
    workspace_id: str,
) -> dict:
    """Retrieve workspace details and extract configuration properties.

    Filters terraform_variables and environment_variables by value_type (string/secret).

    Args:
        client: HarnessClient instance.
        account_id: Account identifier.
        org: Organization identifier.
        project: Project identifier.
        workspace_id: Workspace identifier to retrieve.

    Returns:
        dict: Dictionary with 6 variables:
            - TF_VARIABLES_STRING, TF_VARIABLES_SECRET (filtered terraform_variables)
            - TFENV_VARIABLES_STRING, TFENV_VARIABLES_SECRET (filtered environment_variables)
            - REPOSITORY_CONFIG, PROVISIONER_CONFIG (unchanged)

    Raises:
        ValueError: If workspace not found.
        Exception: For API/network errors.
    """
    scope = Scope(account_id=account_id, org=org, project=project)

    logger.info(f"Querying workspace '{workspace_id}' in org='{org}', project='{project}'")

    try:
        workspace = client.workspaces.get(identifier=workspace_id, scope=scope)
    except Exception as e:
        logger.error(f"Error retrieving workspace '{workspace_id}': {e}")
        raise

    if not workspace or (isinstance(workspace, dict) and not workspace):
        error_msg = f"Workspace '{workspace_id}' not found in org='{org}', project='{project}'"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.debug(f"Retrieved workspace: {workspace.identifier}")

    # Extract and filter TF_VARIABLES by value_type
    tf_variables_raw = getattr(workspace, "terraform_variables", {}) or {}
    tf_variables_string = filter_variables_by_type(tf_variables_raw, "string")
    tf_variables_secret = filter_variables_by_type(tf_variables_raw, "secret")
    logger.debug(f"TF_VARIABLES_STRING: {len(tf_variables_string)} entries")
    logger.debug(f"TF_VARIABLES_SECRET: {len(tf_variables_secret)} entries (values redacted)")

    # Extract and filter TFENV_VARIABLES by value_type
    tfenv_variables_raw = getattr(workspace, "environment_variables", {}) or {}
    tfenv_variables_string = filter_variables_by_type(tfenv_variables_raw, "string")
    tfenv_variables_secret = filter_variables_by_type(tfenv_variables_raw, "secret")
    logger.debug(f"TFENV_VARIABLES_STRING: {len(tfenv_variables_string)} entries")
    logger.debug(f"TFENV_VARIABLES_SECRET: {len(tfenv_variables_secret)} entries (values redacted)")

    # Extract REPOSITORY_CONFIG
    repository_config = {
        "repository": getattr(workspace, "repository", "") or "",
        "repository_branch": getattr(workspace, "repository_branch", "") or "",
        "repository_commit": getattr(workspace, "repository_commit", "") or "",
        "repository_connector": getattr(workspace, "repository_connector", "") or "",
        "repository_path": getattr(workspace, "repository_path", "") or "",
        "repository_sha": getattr(workspace, "repository_sha", "") or "",
    }
    logger.debug(f"REPOSITORY_CONFIG: {repository_config}")

    # Extract PROVISIONER_CONFIG
    provisioner_config = {
        "provider_connector": getattr(workspace, "provider_connector", "") or "",
        "provider_connectors": getattr(workspace, "provider_connectors", "") or "",
        "provisioner": getattr(workspace, "provisioner", "") or "",
        "provisioner_configuration": getattr(workspace, "provisioner_configuration", {}) or {},
        "provisioner_version": getattr(workspace, "provisioner_version", "") or "",
    }
    logger.debug(f"PROVISIONER_CONFIG: {repository_config}")

    return {
        "TF_VARIABLES_STRING": tf_variables_string,
        "TF_VARIABLES_SECRET": tf_variables_secret,
        "TFENV_VARIABLES_STRING": tfenv_variables_string,
        "TFENV_VARIABLES_SECRET": tfenv_variables_secret,
        "REPOSITORY_CONFIG": repository_config,
        "PROVISIONER_CONFIG": provisioner_config,
    }


def export_env_variables(workspace_config: dict) -> str:
    """Generate POSIX shell export format for environment variables.

    Args:
        workspace_config: Dictionary with 6 configuration objects (string/secret variables + configs).

    Returns:
        str: Shell export commands in order: TF_VARIABLES_*, TFENV_VARIABLES_*, then configs.
    """
    export_lines = []

    for var_name, var_value in workspace_config.items():
        # Serialize to JSON string
        json_str = json.dumps(var_value, separators=(",", ":"))
        # Use single quotes to prevent shell interpolation
        export_line = f"export {var_name}='{json_str}'"
        export_lines.append(export_line)

    return "\n".join(export_lines)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Retrieve IACM workspace details and export as environment variables",
        epilog="""
Configuration Sources (precedence: CLI > environment > .harness.yaml):
  --project or HARNESS_PROJECT_ID
  --workspace or HARNESS_WORKSPACE_ID
  --org or HARNESS_ORG_ID (default: "default")
  --debug or DEBUG_MODE (true/false)

Harness Credentials (from environment or .harness.yaml):
  HARNESS_URI (base URL, e.g., https://app.harness.io)
  HARNESS_ACCOUNT_ID (account identifier)
  HARNESS_API_KEY (API authentication token)

Example (environment only):
  export HARNESS_URI="https://app.harness.io"
  export HARNESS_ACCOUNT_ID="account123"
  export HARNESS_API_KEY="pat_token"
  export HARNESS_PROJECT_ID="myproject"
  export HARNESS_WORKSPACE_ID="myworkspace"
  python Return_IACM_Workspace_Details.py
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project",
        default=None,
        help="Project identifier (or set HARNESS_PROJECT_ID)",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Workspace identifier to retrieve (or set HARNESS_WORKSPACE_ID)",
    )
    parser.add_argument(
        "--org",
        default="default",
        help="Organization identifier (default: 'default', or set HARNESS_ORG_ID)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (or set DEBUG_MODE=true)",
    )

    args = parser.parse_args()

    # Early parameter resolution to enable debug logging if needed
    try:
        project, workspace, org, debug = resolve_parameters(args)
    except ValueError as e:
        logger.error(f"Parameter error: {e}")
        return 1

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.debug(f"Parameters resolved: project={project}, workspace={workspace}, org={org}, debug={debug}")

    try:
        config = resolve_config_from_sources()
        logger.debug("Configuration loaded successfully")

        with HarnessClient(config) as client:
            workspace_config = get_workspace_details(
                client,
                account_id=config.account_id,
                org=org,
                project=project,
                workspace_id=workspace,
            )

            export_output = export_env_variables(workspace_config)
            print(export_output)

            return 0

    except ValueError as e:
        logger.error(f"Configuration or workspace error: {e}")
        return 2 if "not found" in str(e).lower() else 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=debug)
        return 3


if __name__ == "__main__":
    sys.exit(main())
