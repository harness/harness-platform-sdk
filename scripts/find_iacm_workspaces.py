#!/usr/bin/env python3
"""Find IACM workspaces by project and workspace state.

This script connects to a remote Harness account and lists all workspaces
in a specified project with a given workspace state.

Usage:
    python find_iacm_workspaces.py --project myproject --state "active"
"""

import argparse
import json
import logging
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


def load_config() -> HarnessConfig:
    """Load Harness configuration from .harness.yaml file.

    Returns:
        HarnessConfig: Configuration object with API credentials.

    Raises:
        FileNotFoundError: If .harness.yaml is not found.
        ValueError: If configuration is invalid.
    """
    config_file_path = Path(__file__).resolve().parent.parent / ".harness.yaml"

    if not config_file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    logger.info(f"Loading configuration from {config_file_path}")
    with open(config_file_path, "r") as file:
        config_data = yaml.safe_load(file)

    if not config_data:
        raise ValueError("Configuration file is empty")

    return HarnessConfig(**config_data)


def find_workspaces_by_state(
    client: HarnessClient,
    account_id: str,
    org: str,
    project: str,
    target_state: str,
) -> list[dict]:
    """Find all workspaces in a project with a specific state.

    Args:
        client: HarnessClient instance.
        account_id: Account identifier.
        org: Organization identifier.
        project: Project identifier.
        target_state: Workspace state to filter by (e.g., "active", "inactive").

    Returns:
        list[dict]: List of workspace details matching the criteria.
    """
    scope = Scope(account_id=account_id, org=org, project=project)
    workspaces = []

    logger.info(f"Querying workspaces in org={org}, project={project}")

    try:
        for workspace in client.workspaces.list(scope=scope):
            logger.debug(f"Found workspace: {workspace.identifier} with status: {workspace.status}")

            if workspace.status and workspace.status.lower() == target_state.lower():
                workspace_detail = {
                    "identifier": workspace.identifier,
                    "name": workspace.name,
                    "status": workspace.status,
                    "provisioner": getattr(workspace, "provisioner", None),
                    "provider_connector": getattr(workspace, "provider_connector", None),
                    "created": getattr(workspace, "created", None),
                }
                workspaces.append(workspace_detail)
                logger.info(
                    f"Matched workspace: {workspace.identifier} (name: {workspace.name}, "
                    f"status: {workspace.status})"
                )

    except Exception as e:
        logger.error(f"Error querying workspaces: {e}")
        raise

    return workspaces


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Find IACM workspaces by project and workspace state"
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Project identifier",
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Workspace state to filter by (e.g., 'active', 'inactive')",
    )
    parser.add_argument(
        "--org",
        default="default",
        help="Organization identifier (default: 'default')",
    )
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="table",
        help="Output format (default: 'table')",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.debug(f"Arguments: project={args.project}, state={args.state}, org={args.org}")

    try:
        config = load_config()
        logger.debug(f"Configuration loaded successfully")

        with HarnessClient(config) as client:
            workspaces = find_workspaces_by_state(
                client,
                account_id=config.account_id,
                org=args.org,
                project=args.project,
                target_state=args.state,
            )

            if args.format == "json":
                print(json.dumps(workspaces, indent=2))
            else:
                if not workspaces:
                    print(f"No workspaces found in project '{args.project}' with state '{args.state}'")
                else:
                    print(f"\nFound {len(workspaces)} workspace(s):")
                    print("-" * 80)
                    for ws in workspaces:
                        print(f"  Identifier: {ws['identifier']}")
                        print(f"  Name:       {ws['name']}")
                        print(f"  Status:     {ws['status']}")
                        print(f"  Provisioner: {ws['provisioner']}")
                        print(f"  Provider:   {ws['provider_connector']}")
                        print(f"  Created:    {ws['created']}")
                        print()
                        # client.workspaces.delete(ws["identifier"],scope=Scope(account_id=config.account_id, org=args.org, project=args.project))

            return 0

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Invalid configuration: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=args.debug)
        return 1


if __name__ == "__main__":
    sys.exit(main())
