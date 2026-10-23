####################
# InputSetV0 Tests
####################

# Test Suite Control InputSetV0
SUITE_NAME = "InputSetV0"
SUITE_TEST_ID = "SDK_Test_InputSetV0"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.input_sets_v0
SUITE_CREATE_OBJECT = InputSetV0CreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    pipeline_identifier=global_project_pipeline_id,
    description="a test",
    variables=[
        {
            "name": "test",
            "type": "String",
            "description": "",
            "required": False,
            "value": "<+input>",
        }
    ],
)

LIST_KWARGS = {"pipeline_identifier": global_project_pipeline_id}
GET_KWARGS = {"pipeline_identifier": global_project_pipeline_id}
DELETE_KWARGS = {"pipeline_identifier": global_project_pipeline_id}

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
