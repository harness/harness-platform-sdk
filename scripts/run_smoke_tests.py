"""
Smoke Tests Runner

This script orchestrates end-to-end integration tests for the Harness Platform SDK.
It dynamically loads and executes test modules organized by tier (dependency order),
using a Harness API client authenticated with environment variables.

The runner injects fixture scope variables (org ID, project ID, etc.) into each test
module's global namespace, enabling tests to reference a shared set of pre-provisioned
Harness resources. Test execution order is controlled via `.test_order.yaml`.

Environment Requirements:
  - HARNESS_PLATFORM_API_KEY: API key for authentication (required)
  - HARNESS_ACCOUNT_ID: Account ID (required)
  - HARNESS_ENDPOINT: Base URL for Harness API (optional, defaults to https://app.harness.io)

Examples:
  # Run all tests
  python scripts/run_smoke_tests.py

  # Run only organization tests
  python scripts/run_smoke_tests.py --filter-type organizations

  # Run all tests and delete created resources
  python scripts/run_smoke_tests.py --cleanup

  # Run tests and delete both created and unit-level resources
  python scripts/run_smoke_tests.py --cleanup --unit-cleanup
"""
from os import environ
from pathlib import Path
import argparse
import yaml

from harness_platform_sdk import HarnessClient, HarnessConfig, Scope, ApiError
from harness_platform_sdk.models.ng_api import *
from harness_platform_sdk.models.authz import *
from harness_platform_sdk.models.pipeline_api import *
from harness_platform_sdk.models.template_api import *
from harness_platform_sdk.models.iacm_api import *
from harness_platform_sdk.models.idp_api import *


def create_argument_parser():
  """Parse command-line arguments for smoke test execution."""
  parser = argparse.ArgumentParser(
      description="Execute Harness Platform SDK smoke tests"
  )
  parser.add_argument(
      '--filter-type',
      type=str,
      default=None,
      required=False,
      help='Run only tests matching this classification (e.g., organizations, projects, pipelines). If omitted, runs all tests in tier order.'
  )
  parser.add_argument(
      '--cleanup',
      action='store_true',
      help='Delete resources created during test execution (test-scoped cleanup).'
  )
  parser.add_argument(
      '--unit-cleanup',
      action='store_true',
      help='Delete both test-scoped and unit-scoped resources. Implies --cleanup.'
  )
  parser.add_argument(
      '--skip-fixtures',
      action='store_true',
      help='Do not load pre-provisioned fixture scope (advanced: use only if fixtures are unavailable).'
  )
  return parser


def load_smoke_test_module(module_path, globals_dict):
  """
  Dynamically load and execute a Python test module in the given global namespace.

  Args:
    module_path (Path): Absolute path to the .py test module
    globals_dict (dict): Global namespace where the module executes. This typically
                        includes the HarnessClient, fixture scope variables, etc.
  """
  with open(module_path, 'r') as f:
    code = f.read()
  exec(compile(code, str(module_path), 'exec'), globals_dict)

def validate_environment():
  """
  Validate required environment variables for test execution.

  Raises:
    Exception: If HARNESS_PLATFORM_API_KEY or HARNESS_ACCOUNT_ID are not set.
  """
  if not environ.get("HARNESS_PLATFORM_API_KEY", False) or not environ.get("HARNESS_ACCOUNT_ID", False):
    raise Exception(
        "Required environment variables missing:\n"
        "  - HARNESS_PLATFORM_API_KEY: API key for authentication\n"
        "  - HARNESS_ACCOUNT_ID: Harness account ID\n\n"
        "Optional:\n"
        "  - HARNESS_ENDPOINT: Base URL (defaults to https://app.harness.io)"
    )


def create_harness_config():
  """
  Create a HarnessConfig from environment variables.

  Returns:
    HarnessConfig: Configured client ready for use.
  """
  return HarnessConfig(
      api_key=environ.get("HARNESS_PLATFORM_API_KEY", "MISSING-API-KEY"),
      account_id=environ.get("HARNESS_ACCOUNT_ID", "MISSING-ACCOUNT-ID"),
      base_url=environ.get("HARNESS_ENDPOINT", "https://app.harness.io"),
  )


def load_test_ordering(smoke_test_dir):
  """
  Load test execution order from .test_order.yaml.

  Args:
    smoke_test_dir (Path): Directory containing tests and .test_order.yaml

  Returns:
    dict: Test tier mapping (tier_name -> [test_module_names])

  Raises:
    Exception: If .test_order.yaml does not exist.
  """
  test_order_path = smoke_test_dir / ".test_order.yaml"
  if not test_order_path.exists():
    raise Exception(
        f"Test order file not found: {test_order_path}\n"
        "Expected structure: <tier>: [test_module_name_1, ...]"
    )
  with open(test_order_path, 'r') as f:
    return yaml.safe_load(f)


def normalize_test_module_name(test_suite_name):
  """
  Normalize a test module name by ensuring .py extension.

  Args:
    test_suite_name (str): Test module name with or without .py extension

  Returns:
    str: Test module name with .py extension
  """
  if not test_suite_name.endswith('.py'):
    return f"{test_suite_name}.py"
  return test_suite_name


def main():
  """Main entry point for smoke test orchestration."""
  parser = create_argument_parser()
  args = parser.parse_args()

  validate_environment()

  working_dir = Path(__file__).resolve().parent.parent
  smoke_test_dir = working_dir / "tests" / "smoke"

  config = create_harness_config()
  test_ordering = load_test_ordering(smoke_test_dir)

  fixture_scope = {
      "global_org_id": "PLATFORM_SDK_FIXTURES",
      "global_org_name": "Platform Sdk Fixtures",
      "global_project_id": "FIXTURE_PLACEHOLDER",
      "global_project_name": "Fixture Placeholder",
      "global_project_pipeline_id": "default_list_pipeline",
      "global_project_environment_id": "default_list_environment",
      "global_project_connector": "default_list_connector",
      "global_project_secret": "default_list_secret",
      "global_project_workspace": "default_list_workspace",
      "global_catalog_entity": "default_idp_catalog_entity",
      "global_idp_scorecard_check": "default_idp_scorecard_check",
      "global_idp_scorecard": "default_idp_scorecard",
  }

  with HarnessClient(config) as client:
    client.set_default_scope(
        org=fixture_scope["global_org_id"],
        project=fixture_scope["global_project_id"]
    )

    test_globals = {**globals(), "client": client,"cleanup":args.cleanup, **fixture_scope}

    for tier_level, test_suites in test_ordering.items():
      print(f"{f'~~ {tier_level.upper()} ~~':*^40}")
      if not test_suites:
        print("No tests at this tier")
        continue

      for test_suite_name in test_suites:
        test_module_name = normalize_test_module_name(test_suite_name)
        test_module_path = smoke_test_dir / test_module_name

        if args.filter_type is not None:
          test_label = test_module_name.replace(".py", "")
          if args.filter_type != test_label:
            continue

        try:
          load_smoke_test_module(test_module_path, test_globals)
        except Exception as e:
          print(f"✗ {test_module_name}: {e}")
          raise

        if args.filter_type is not None:
          break


if __name__ == "__main__":
  main()
