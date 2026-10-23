####################
# Entities Tests
####################

# Test Suite Control Entities
SUITE_NAME = "Entities"
SUITE_TEST_ID = "SDK_Test_Entities"
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.entities
SUITE_CREATE_OBJECT = EntityResourceCreateRequest(
    identifier=SUITE_TEST_ID,
    name=SUITE_TEST_NAME,
    description="a test",
    lifecycle="production",
    type="sdk_test",
    owner="test",
)

LIST_KWARGS = {}
GET_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}
UPDATE_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}
DELETE_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}

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
        identifier=validation_object.identifier, body=test_create_request, **UPDATE_KWARGS
    )
    print(f"\t -> Updated : {validation_object.identifier}")
print(f"{SUITE_NAME} -> List")
for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
    print(f"\t \t -> : {validate_method_list.identifier}")

if cleanup:
    SUITE_TEST_CLASS.delete(identifier=validation_object.identifier, **DELETE_KWARGS)
    print(f"\t -> Delete : {validation_object.identifier}")
