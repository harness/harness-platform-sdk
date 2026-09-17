#!/usr/bin/env python3
# Copyright (c) 2025 Harness Solution Factory. All Rights Reserved.
"""Clone/migrate an IACM workspace to a new workspace with configurable overrides.

This script retrieves an existing IACM workspace configuration, validates
the target location, applies optional overrides, and creates a new workspace
with the cloned or modified configuration.

Usage:
    python Migrate_Workspace.py --source-project src-proj --source-workspace src-ws \\
      --target-project tgt-proj --target-workspace tgt-ws
    python Migrate_Workspace.py --org myorg --source-project src-proj \\
      --source-workspace src-ws --target-org tgt-org --target-project tgt-proj \\
      --target-workspace tgt-ws --override-file overrides.yaml
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

    config_file_path = Path(__file__).resolve().parent.parent / ".harness.yaml"
    if config_file_path.exists():
        logger.debug(f"Found .harness.yaml at {config_file_path}")
        try:
            with open(config_file_path, "r") as file:
                file_data = yaml.safe_load(file)
            if file_data:
                config_data.update(file_data)
                sources_tried.append("file")
                logger.debug("Loaded config from .harness.yaml")
        except Exception as e:
            logger.warning(f"Failed to load .harness.yaml: {e}")

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

    required_fields = {"base_url", "account_id", "api_key"}
    missing_fields = required_fields - set(config_data.keys())
    if missing_fields:
        raise ValueError(
            f"Missing required configuration fields: {', '.join(missing_fields)}. "
            f"Provide via .harness.yaml or environment variables (HARNESS_URI, HARNESS_ACCOUNT_ID, HARNESS_API_KEY)."
        )

    return HarnessConfig(**config_data)


def resolve_parameters(args) -> tuple[str, str, str, str, str, str, str, bool]:
    """Resolve script parameters from CLI args and environment variables.

    Precedence (highest to lowest):
    1. CLI arguments
    2. Environment variables
    3. Defaults (org="default", target_org=source_org)

    Args:
        args: Parsed command-line arguments from argparse.

    Returns:
        tuple: (org, source_project, source_workspace, target_org, target_project,
                target_workspace, override_file, debug_mode)

    Raises:
        ValueError: If required parameters are missing.
    """
    org = args.org or os.environ.get("HARNESS_ORG_ID", "").strip() or "default"

    source_project = args.source_project or os.environ.get("HARNESS_SOURCE_PROJECT_ID", "").strip()
    if not source_project:
        raise ValueError(
            "Source project ID is required. Provide via --source-project or HARNESS_SOURCE_PROJECT_ID."
        )

    source_workspace = args.source_workspace or os.environ.get("HARNESS_SOURCE_WORKSPACE_ID", "").strip()
    if not source_workspace:
        raise ValueError(
            "Source workspace ID is required. Provide via --source-workspace or HARNESS_SOURCE_WORKSPACE_ID."
        )

    target_project = args.target_project or os.environ.get("HARNESS_TARGET_PROJECT_ID", "").strip()
    if not target_project:
        raise ValueError(
            "Target project ID is required. Provide via --target-project or HARNESS_TARGET_PROJECT_ID."
        )

    target_workspace = args.target_workspace or os.environ.get("HARNESS_TARGET_WORKSPACE_ID", "").strip()
    if not target_workspace:
        raise ValueError(
            "Target workspace ID is required. Provide via --target-workspace or HARNESS_TARGET_WORKSPACE_ID."
        )

    target_org = args.target_org or os.environ.get("HARNESS_TARGET_ORG_ID", "").strip() or org

    override_file = args.override_file or os.environ.get("HARNESS_OVERRIDE_FILE", "").strip() or None

    debug = args.debug
    if not debug:
        debug_env = os.environ.get("DEBUG_MODE", "").strip()
        debug = debug_env.lower() in ("true", "1")

    logger.debug(
        f"Resolved parameters: org={org}, source_project={source_project}, "
        f"source_workspace={source_workspace}, target_org={target_org}, "
        f"target_project={target_project}, target_workspace={target_workspace}, "
        f"override_file={override_file}, debug={debug}"
    )

    return org, source_project, source_workspace, target_org, target_project, target_workspace, override_file, debug


def output_result(status: str, data: dict = None, error_code: int = None, exit_code: int = 0):
    """Output result as JSON and exit.

    Args:
        status: "success" or "error"
        data: Additional data to include in output
        error_code: Error code (1, 2, or 3) for error status
        exit_code: System exit code
    """
    output = {"status": status}

    if status == "success":
        output.update(data or {})
    else:
        output["error_code"] = error_code
        output.update(data or {})

    print(json.dumps(output))
    sys.exit(exit_code)


def load_override_file(file_path: str) -> dict:
    """Load and parse override file (YAML or JSON).

    Args:
        file_path: Path to override file.

    Returns:
        dict: Parsed override configuration.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file parsing fails or contains invalid keys.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Override file not found: {file_path}")

    try:
        with open(path, "r") as f:
            if file_path.endswith(".json"):
                overrides = json.load(f)
            else:
                overrides = yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse override file: {e}")

    if not overrides:
        logger.debug("Override file is empty, no overrides will be applied")
        return {}

    allowed_keys = {
        "provider_connector",
        "provider_connectors",
        "provisioner",
        "provisioner_configuration",
        "provisioner_version",
        "prune_sensitive_data",
        "repository_branch",
        "repository_commit",
        "repository_connector",
        "repository_path",
        "repository_sha",
        "repository_submodules",
        "terraform_variable_files",
        "terraform_variables",
        "variable_sets",
    }

    invalid_keys = set(overrides.keys()) - allowed_keys
    if invalid_keys:
        logger.warning(f"Override file contains unknown keys (will be ignored): {invalid_keys}")

    logger.info(f"Loaded {len(overrides)} override(s) from {file_path}")
    return {k: v for k, v in overrides.items() if k in allowed_keys}


def deep_merge(source: dict, overrides: dict) -> dict:
    """Deep merge override values into source dictionary.

    For nested dicts, recursively merge. For lists and other types, override.

    Args:
        source: Base configuration dictionary.
        overrides: Override values to merge in.

    Returns:
        dict: Merged configuration.
    """
    result = source.copy()

    for key, override_value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(override_value, dict):
            result[key] = deep_merge(result[key], override_value)
        else:
            result[key] = override_value

    return result


def extract_workspace_config(workspace) -> dict:
    """Extract complete workspace configuration from workspace object.

    Args:
        workspace: Workspace object returned from API.

    Returns:
        dict: Configuration dictionary suitable for cloning.
    """
    config = {}

    field_mappings = {
        "provider_connector",
        "provider_connectors",
        "provisioner",
        "provisioner_configuration",
        "provisioner_version",
        "prune_sensitive_data",
        "repository",
        "repository_branch",
        "repository_commit",
        "repository_connector",
        "repository_path",
        "repository_sha",
        "repository_submodules",
        "terraform_variable_files",
        "terraform_variables",
        "variable_sets",
        "name",
        "description",
        "environment_variables",
    }

    for field in field_mappings:
        value = getattr(workspace, field, None)
        if value is not None:
            config[field] = value

    logger.debug(f"Extracted {len(config)} configuration fields from source workspace")
    return config


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Clone/migrate an IACM workspace to a new workspace with configurable overrides",
        epilog="""
Configuration Sources (precedence: CLI > environment > .harness.yaml):
  --org or HARNESS_ORG_ID (default: "default")
  --source-project or HARNESS_SOURCE_PROJECT_ID (required)
  --source-workspace or HARNESS_SOURCE_WORKSPACE_ID (required)
  --target-org or HARNESS_TARGET_ORG_ID (default: same as --org)
  --target-project or HARNESS_TARGET_PROJECT_ID (required)
  --target-workspace or HARNESS_TARGET_WORKSPACE_ID (required)
  --override-file or HARNESS_OVERRIDE_FILE (optional YAML/JSON)
  --debug or DEBUG_MODE (true/false)

Harness Credentials (from environment or .harness.yaml):
  HARNESS_URI, HARNESS_ACCOUNT_ID, HARNESS_API_KEY

Example:
  python Migrate_Workspace.py \\
    --source-project myproject \\
    --source-workspace source-ws \\
    --target-project myproject \\
    --target-workspace cloned-ws \\
    --override-file overrides.yaml
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--org",
        default=None,
        help="Source organization identifier (default: 'default', or set HARNESS_ORG_ID)",
    )
    parser.add_argument(
        "--source-project",
        default=None,
        help="Source project identifier (or set HARNESS_SOURCE_PROJECT_ID)",
    )
    parser.add_argument(
        "--source-workspace",
        default=None,
        help="Source workspace identifier to clone from (or set HARNESS_SOURCE_WORKSPACE_ID)",
    )
    parser.add_argument(
        "--target-org",
        default=None,
        help="Target organization identifier (default: same as --org, or set HARNESS_TARGET_ORG_ID)",
    )
    parser.add_argument(
        "--target-project",
        default=None,
        help="Target project identifier (or set HARNESS_TARGET_PROJECT_ID)",
    )
    parser.add_argument(
        "--target-workspace",
        default=None,
        help="Target workspace identifier for new workspace (or set HARNESS_TARGET_WORKSPACE_ID)",
    )
    parser.add_argument(
        "--override-file",
        default=None,
        help="Path to YAML or JSON file with configuration overrides (or set HARNESS_OVERRIDE_FILE)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (or set DEBUG_MODE=true)",
    )

    args = parser.parse_args()

    try:
        org, source_project, source_workspace, target_org, target_project, target_workspace, override_file, debug = resolve_parameters(
            args
        )
    except ValueError as e:
        logger.error(f"Parameter error: {e}")
        output_result(
            "error",
            {"error_message": str(e), "details": {}},
            error_code=1,
            exit_code=1,
        )

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        config = resolve_config_from_sources()
        logger.debug("Configuration loaded successfully")

        overrides = None
        if override_file:
            try:
                overrides = load_override_file(override_file)
            except FileNotFoundError as e:
                logger.error(f"Override file error: {e}")
                output_result(
                    "error",
                    {
                        "error_message": str(e),
                        "details": {"override_file": override_file},
                    },
                    error_code=1,
                    exit_code=1,
                )
            except ValueError as e:
                logger.error(f"Override file parsing error: {e}")
                output_result(
                    "error",
                    {
                        "error_message": str(e),
                        "details": {"override_file": override_file},
                    },
                    error_code=1,
                    exit_code=1,
                )

        with HarnessClient(config) as client:
            source_scope = Scope(account_id=config.account_id, org=org, project=source_project)

            logger.info(f"Retrieving source workspace '{source_workspace}' from {org}/{source_project}")
            try:
                source_workspace_obj = client.workspaces.get(identifier=source_workspace, scope=source_scope)
            except Exception as e:
                logger.error(f"Error retrieving source workspace: {e}")
                output_result(
                    "error",
                    {
                        "error_message": f"Failed to retrieve source workspace '{source_workspace}': {e}",
                        "details": {"workspace_id": source_workspace, "org": org, "project": source_project},
                    },
                    error_code=3,
                    exit_code=3,
                )

            if not source_workspace_obj or (isinstance(source_workspace_obj, dict) and not source_workspace_obj):
                error_msg = f"Source workspace '{source_workspace}' not found in {org}/{source_project}"
                logger.error(error_msg)
                output_result(
                    "error",
                    {
                        "error_message": error_msg,
                        "details": {"workspace_id": source_workspace, "org": org, "project": source_project},
                    },
                    error_code=1,
                    exit_code=1,
                )

            logger.info(
                f"Source workspace found: identifier={source_workspace_obj.identifier}, "
                f"name={getattr(source_workspace_obj, 'name', 'N/A')}, "
                f"status={getattr(source_workspace_obj, 'status', 'N/A')}, "
                f"provisioner={getattr(source_workspace_obj, 'provisioner', 'N/A')}"
            )

            if org == target_org and source_project == target_project and source_workspace == target_workspace:
                error_msg = "Target workspace is identical to source; cannot clone to same location"
                logger.error(error_msg)
                output_result(
                    "error",
                    {
                        "error_message": error_msg,
                        "details": {"source": source_workspace, "target": target_workspace},
                    },
                    error_code=2,
                    exit_code=2,
                )

            if org == target_org and source_project == target_project:
                logger.debug(f"Target is in same org/project; checking for existing workspace '{target_workspace}'")
                target_scope = Scope(account_id=config.account_id, org=target_org, project=target_project)
                try:
                    existing_workspace = client.workspaces.get(identifier=target_workspace, scope=target_scope)
                    if existing_workspace and (
                        not isinstance(existing_workspace, dict) or bool(existing_workspace)
                    ):
                        error_msg = (
                            f"Workspace '{target_workspace}' already exists in {target_org}/{target_project}"
                        )
                        logger.error(error_msg)
                        output_result(
                            "error",
                            {
                                "error_message": error_msg,
                                "details": {"target_workspace": target_workspace, "org": target_org, "project": target_project},
                            },
                            error_code=2,
                            exit_code=2,
                        )
                except Exception as e:
                    if "not found" not in str(e).lower():
                        logger.debug(f"Checking target workspace returned: {e}")

            workspace_config = extract_workspace_config(source_workspace_obj)

            if override_file and overrides:
                workspace_config = deep_merge(workspace_config, overrides)
                logger.info(f"Applied {len(overrides)} override(s) to workspace configuration")

            workspace_config["identifier"] = target_workspace
            if "name" not in workspace_config:
                workspace_config["name"] = target_workspace

            target_scope = Scope(account_id=config.account_id, org=target_org, project=target_project)

            logger.info(f"Creating target workspace '{target_workspace}' in {target_org}/{target_project}")
            try:
                created_workspace = client.workspaces.create(workspace_config, scope=target_scope)
            except Exception as e:
                logger.error(f"Error creating target workspace: {e}")
                output_result(
                    "error",
                    {
                        "error_message": f"Failed to create target workspace: {e}",
                        "details": {
                            "target_workspace": target_workspace,
                            "org": target_org,
                            "project": target_project,
                        },
                    },
                    error_code=3,
                    exit_code=3,
                )

            if not created_workspace or not getattr(created_workspace, "identifier", None):
                error_msg = "Workspace creation returned empty or invalid response"
                logger.error(error_msg)
                output_result(
                    "error",
                    {
                        "error_message": error_msg,
                        "details": {"target_workspace": target_workspace},
                    },
                    error_code=3,
                    exit_code=3,
                )

            logger.info(f"Target workspace created successfully: {created_workspace.identifier}")

            output_result(
                "success",
                {
                    "workspace_id": created_workspace.identifier,
                    "org": target_org,
                    "project": target_project,
                    "message": f"Successfully created workspace '{created_workspace.identifier}' in {target_org}/{target_project}",
                },
                exit_code=0,
            )

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        output_result(
            "error",
            {
                "error_message": str(e),
                "details": {},
            },
            error_code=1,
            exit_code=1,
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=debug)
        output_result(
            "error",
            {
                "error_message": f"Unexpected error: {e}",
                "details": {},
            },
            error_code=3,
            exit_code=3,
        )


if __name__ == "__main__":
    sys.exit(main())
