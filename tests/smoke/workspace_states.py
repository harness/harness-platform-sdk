####################
# WorkspaceStates Tests
####################

# Test Suite Control WorkspaceStates
SUITE_NAME = "WorkspaceStates"
SUITE_TEST_ID = "SDK_Test_WorkspaceStates"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.workspace_states
SUITE_CREATE_OBJECT = WorkspaceStateCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    terraform_version="1.10.0",
    lineage="4",
    version="4",
    resources=[
        {
            "mode": "data",
            "type": "harness_platform_organization",
            "name": "selected",
            "provider": 'provider["registry.opentofu.org/harness/harness"]',
            "instances": [
                {
                    "schema_version": 4,
                    "attributes": {
                        "description": "Centralized Harness Platform Management",
                        "id": "Harness_Platform_Management",
                        "identifier": "Harness_Platform_Management",
                        "name": "Harness Platform Management",
                        "tags": [
                            "created_by:Terraform",
                            "harnessSolutionsFactory:true",
                            "managedResource:true",
                        ],
                    },
                    "sensitive_attributes": [],
                }
            ],
        },
    ],
)
workspaces_request = WorkspaceCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="a test",
    provisioner="opentofu",
    repository="goodrum-harness/terraform-provider-harness",
    repository_connector=global_project_connector,
    repository_branch="main",
    repository_path="examples/resources/harness_platform_organization",
)

print(f"{f" {SUITE_NAME} ":#^40}")
print(f"{SUITE_NAME} -> PreWork")
workspace = client.workspaces.get(
    identifier=workspaces_request.identifier,
)

if not workspace:
    workspace = client.workspaces.create(workspaces_request)
    print(f"\t -> Created PreWork Workspace : { workspace.identifier}")

LIST_KWARGS = {"workspace_identifier": global_project_workspace}
GET_KWARGS = {}
DELETE_KWARGS = {"workspace_identifier": global_project_workspace}

print(f"{SUITE_NAME} -> List")
if hasattr(SUITE_TEST_CLASS, "list"):
    for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
        print(f"\t \t -> : {validate_method_list.identifier}")
else:
    print(f"\t \t Skip Method 'List' as not a valid method")

test_create_request = SUITE_CREATE_OBJECT
validation_object = SUITE_TEST_CLASS.get(identifier=test_create_request.identifier, **GET_KWARGS)
if validation_object:
    print(f"\t -> Get : {validation_object.identifier}")
    test_create_request.description = "Smoke Test Validation - Update"
    validation_object = SUITE_TEST_CLASS.create(
        identifier=validation_object.identifier, body=test_create_request
    )
    print(f"\t -> Created : {validation_object.identifier}")
else:
    validation_object = SUITE_TEST_CLASS.create(
        identifier=test_create_request.identifier, body=test_create_request
    )
    print(f"\t -> Created : {validation_object.identifier}")
print(f"{SUITE_NAME} -> List")
if hasattr(SUITE_TEST_CLASS, "list"):
    for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
        print(f"\t \t -> : {validate_method_list.identifier}")
else:
    print(f"\t \t Skip Method 'List' as not a valid method")

if cleanup:
    client.workspaces.delete(workspaces_request.identifier)
    print(f"\t -> Delete PreWork Workspace : {workspaces_request.identifier}")
