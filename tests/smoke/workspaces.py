####################
# Workspaces Tests
####################

# Test Suite Control Workspaces
SUITE_NAME = "Workspaces"
SUITE_TEST_ID = "SDK_Test_Workspaces"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.workspaces
SUITE_CREATE_OBJECT = WorkspaceCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="a test",
    provisioner="opentofu",
    repository="goodrum-harness/terraform-provider-harness",
    repository_connector=global_project_connector,
    repository_branch="main",
    repository_path="examples/resources/harness_platform_organization",
    environment_variables={
        "HARNESS_ACCOUNT_ID": {
            "key": "HARNESS_ACCOUNT_ID",
            "value": client._config.account_id,
            "value_type": "string",
        },
        "HARNESS_PLATFORM_API_KEY": {
            "key": "HARNESS_PLATFORM_API_KEY",
            "value": global_project_secret,
            "value_type": "secret",
        },
    },
    terraform_variables={
        "HARNESS_ENDPOINT": {
            "key": "HARNESS_ENDPOINT",
            "value": client._config.base_url,
            "value_type": "string",
        },
    },
)

LIST_KWARGS = {}
GET_KWARGS = {}
DELETE_KWARGS = {}

print(f"{f" {SUITE_NAME} ":#^40}")
print(f"{SUITE_NAME} -> List")
for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
    print(f"\t \t -> : {validate_method_list.identifier}")

test_create_request = SUITE_CREATE_OBJECT
validation_object = SUITE_TEST_CLASS.get(identifier=test_create_request.identifier, **GET_KWARGS)
if validation_object:
    print(f"\t -> Get : {validation_object.identifier}")
    test_create_request.description = "Smoke Test Validation - Update"
    validation_object = SUITE_TEST_CLASS.update(
        identifier=validation_object.identifier, body=test_create_request
    )
    print(f"\t -> Updated : {validation_object.identifier}")

else:
    validation_object = SUITE_TEST_CLASS.create(test_create_request)
    print(f"\t -> Created : {validation_object.identifier}")
    validation_object.description = "Smoke Test Validation - Update after create"
    validation_object = SUITE_TEST_CLASS.update(
        identifier=validation_object.identifier, body=test_create_request
    )
    print(f"\t -> Updated : {validation_object.identifier}")
print(f"{SUITE_NAME} -> List")
for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
    print(f"\t \t -> : {validate_method_list.identifier}")

if cleanup:
    SUITE_TEST_CLASS.delete(identifier=validation_object.identifier, **DELETE_KWARGS)
    print(f"\t -> Delete : {validation_object.identifier}")
