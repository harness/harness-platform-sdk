# GENERATED — do not edit. Run mise run regenerate to update.
from pathlib import Path
import argparse
import yaml

from harness_python_sdk import HarnessClient, HarnessConfig, Scope, ApiError
# from harness_python_sdk.api import PipelinesApi,ConnectorsApi,SecretsApi
from harness_python_sdk.models.ng_api import *
from harness_python_sdk.models.authz import *
from harness_python_sdk.models.pipeline_api import *
from harness_python_sdk.models.template_api import *
from harness_python_sdk.models.iacm_api import *
from harness_python_sdk.models.idp_api import *

parser = argparse.ArgumentParser(
    description="Execute Smoke Tests"
)
parser.add_argument(
    '--filter-type',
    type=str,
    default=None,
    required=False,
    help='Provide the specific filter classification to test - e.g. organizations, projects, pipelines'
)
parser.add_argument(
    '--cleanup',
    action='store_true',
    help='Should the resources be deleted as well?'
)
parser.add_argument(
    '--unit-cleanup',
    action='store_true',
    help='Should the unit resources be deleted as well?'
)
parser.add_argument(
    '--skip-fixtures',
    action='store_true',
    help='Should skip the default fixtures?'
)

args = parser.parse_args()
cleanup = args.cleanup
unit_cleanup = args.unit_cleanup
# Create a client
working_dir=Path(__file__).resolve().parent.parent
config_file_path = Path(working_dir).joinpath(".harness.yaml")
if not config_file_path.exists:
    raise Exception("No Configuration file exists")
with open(config_file_path, 'r') as file:
    config_file = yaml.safe_load(file)
config = HarnessConfig(**config_file)

with HarnessClient(config) as client:

    global_org_id="smoke_test"
    global_org_name=global_org_id.replace("_"," ").capitalize()
    global_project_id="smoke_demo"
    global_project_name=global_project_id.replace("_"," ").capitalize()

    smoke_test_dir=Path(working_dir).joinpath("tests","smoke")

    if not args.skip_fixtures:
        # Load Organizations
        with open(Path(smoke_test_dir).joinpath("organizations.py")) as f:
            exec(f.read())

        client.set_default_scope(org=global_org_id)

        # Load Projects
        with open(Path(smoke_test_dir).joinpath("projects.py")) as f:
            exec(f.read())

    client.set_default_scope(org=global_org_id,project=global_project_id)
    if not args.skip_fixtures:
        # Load Pipelines
        with open(Path(smoke_test_dir).joinpath("pipelines_v0.py")) as f:
            exec(f.read())


    glob_files = sorted(smoke_test_dir.glob("*.py"))
    tier_0_file_list = ["organizations.py","projects.py","pipelines_v0.py"]
    tier_2_file_list = [
        "input_sets_v0.py","triggers_v0.py","infrastructures.py",
        "workspace_states.py", "workspace_pre_work", "workspace_default_pipelines",
        "workspace_variables",
    ]
    tier_3_file_list = ["workspace_approvals.py"]
    tiers = [tier_0_file_list, tier_2_file_list, tier_3_file_list]
    ignored_files = [item for sublist in tiers for item in sublist]

    tier_1_files = [elem for elem in glob_files if elem.name not in ignored_files]
    tier_2_files = [elem for elem in glob_files if elem.name in tier_2_file_list]

    if args.filter_type is not None:
        glob_files = [elem for elem in glob_files if elem.name == f"{args.filter_type}.py"]
        for file_path in glob_files:
            with open(Path(smoke_test_dir).joinpath(file_path.name)) as f:
                exec(f.read())
    else:
        print("Processing Tier 1 List")
        for file_path in tier_1_files:
            with open(Path(smoke_test_dir).joinpath(file_path.name)) as f:
                exec(f.read())

        print("Processing Tier 2 List")
        for file_path in tier_2_files:
            with open(Path(smoke_test_dir).joinpath(file_path.name)) as f:
                exec(f.read())


    if cleanup:
        print(f"{' Cleanup ':#^40}")
        client.pipelines_v0.delete(identifier=pipeline.identifier)
        print(f"Pipeline -> Delete : {pipeline.identifier}")
        client.projects.delete(identifier=global_project_id)
        print(f"Projects -> Deleted : {global_project_id}")
        client.organizations.delete(identifier=global_org_id)
        print(f"Organization -> Deleted : {global_org_id}")
